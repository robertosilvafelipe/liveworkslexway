import csv
import hashlib
import io
import json
import logging
import os
import re
import secrets
import time
import unicodedata
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from fastapi import BackgroundTasks, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from . import db, grading, mailer
from .auth import hash_password, verify_password

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

BASE = os.path.dirname(__file__)
TZ = ZoneInfo(os.environ.get("WS_TZ", "America/Sao_Paulo"))
SECRET = os.environ.get("WS_SECRET_KEY", "dev-insecure-secret")
HTTPS = os.environ.get("WS_HTTPS", "0") == "1"
APP_NAME = os.environ.get("WS_APP_NAME", "LexWay Worksheets")
BASE_URL = os.environ.get("WS_BASE_URL", "").rstrip("/")
SCHOOL_EMAIL = os.environ.get("WS_SCHOOL_EMAIL", "lexway.english@gmail.com")
RESET_MINUTES = 60
RESET_ADMIN_HOURS = 72
ROLES = {"admin": "Administrador(a)", "teacher": "Professor(a)", "student": "Aluno(a)"}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=SECRET, session_cookie="ws_session", max_age=60 * 60 * 24 * 14,
                   same_site="lax", https_only=HTTPS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE, "templates"))


@app.middleware("http")
async def origin_check(request: Request, call_next):
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        origin = request.headers.get("origin") or request.headers.get("referer")
        if origin and urlparse(origin).netloc != request.headers.get("host"):
            return Response("Origem inválida", status_code=403)
    resp = await call_next(request)
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


@app.on_event("startup")
def _startup():
    db.init()


# ======================================================================
# helpers
# ======================================================================

class Redirect(Exception):
    def __init__(self, url):
        self.url = url


@app.exception_handler(Redirect)
def _redirect(request, exc):
    return RedirectResponse(exc.url, status_code=303)


def fmt_dt(value, with_time=True):
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(str(value))
    except ValueError:
        return str(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(TZ).strftime("%d/%m/%Y %H:%M" if with_time else "%d/%m/%Y")


def fmt_grade(v):
    return "—" if v is None else f"{v:.1f}".replace(".", ",")


templates.env.filters["dt"] = fmt_dt
templates.env.filters["grade"] = fmt_grade
templates.env.globals.update(TYPES=grading.TYPES, LEVELS=grading.LEVELS, SUBJECTS=grading.SUBJECTS,
                             GRADING=grading.GRADING, SHOW_ANSWERS=grading.SHOW_ANSWERS, APP_NAME=APP_NAME,
                             ROLES=ROLES, SCHOOL_EMAIL=SCHOOL_EMAIL,
                             parse_text=grading.parse_text, to_ten=grading.to_ten)


def flash(request, msg, kind="ok"):
    request.session.setdefault("flash", []).append([kind, msg])


def render(request, name, user=None, **ctx):
    msgs = request.session.pop("flash", [])
    return templates.TemplateResponse(request, name, {"user": user, "messages": msgs, **ctx})


def _pw_marker(user):
    return hashlib.sha256(user["password_hash"].encode()).hexdigest()[:16]


def start_session(request, user):
    request.session.clear()
    request.session["uid"] = user["id"]
    request.session["pv"] = _pw_marker(user)


def current_user(request):
    uid = request.session.get("uid")
    if not uid:
        return None
    u = db.one("SELECT * FROM users WHERE id=? AND active=1", (uid,))
    # a password change (or reset) invalidates every other session of that user
    if not u or request.session.get("pv") != _pw_marker(u):
        request.session.clear()
        return None
    return u


def need(request, *roles):
    u = current_user(request)
    if not u:
        raise Redirect("/login")
    if u["role"] not in roles:
        flash(request, "Você não tem acesso a essa página.", "error")
        raise Redirect("/")
    return u


STAFF = ("admin", "teacher")


def is_admin(u):
    return u["role"] == "admin"


def client_ip(request):
    return request.headers.get("x-forwarded-for", request.client.host if request.client else "?").split(",")[0].strip()


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def clean_email(v):
    v = (v or "").strip().lower()
    if v and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
        raise ValueError("E-mail inválido.")
    return v or None


def clean_username(v):
    v = (v or "").strip().lower()
    if not re.match(r"^[a-z0-9._-]{3,40}$", v):
        raise ValueError("Usuário deve ter 3 a 40 caracteres: letras, números, ponto, hífen ou _.")
    return v


def unique_or_error(username, email, user_id=0):
    if db.one("SELECT id FROM users WHERE username=? AND id<>?", (username, user_id)):
        raise ValueError(f"O usuário '{username}' já existe.")
    if email and db.one("SELECT id FROM users WHERE email=? AND id<>?", (email, user_id)):
        raise ValueError(f"O e-mail {email} já está em uso.")


# ---------- scope (what each staff member can see / manage) ----------

def my_classes(u):
    if is_admin(u):
        return db.all("SELECT * FROM classes ORDER BY level, name")
    return db.all("""SELECT c.* FROM classes c JOIN class_teachers ct ON ct.class_id=c.id
                     WHERE ct.teacher_id=? ORDER BY c.level, c.name""", (u["id"],))


def my_class_ids(u):
    return {c["id"] for c in my_classes(u)}


def load_exercise(eid):
    ex = db.one("SELECT * FROM exercises WHERE id=?", (eid,))
    if ex:
        ex["items"] = json.loads(ex["items"])
        ex["class_ids"] = [r["class_id"] for r in db.all("SELECT class_id FROM exercise_classes WHERE exercise_id=?", (eid,))]
    return ex


def can_manage_exercise(u, ex, classes=None):
    if is_admin(u) or ex.get("created_by") == u["id"]:
        return True
    classes = my_classes(u) if classes is None else classes
    if ex["class_ids"]:
        return bool({c["id"] for c in classes} & set(ex["class_ids"]))
    return ex["level"] in {c["level"] for c in classes}


def managed_exercise_ids(u):
    rows = db.all("SELECT id, level, created_by FROM exercises")
    links = {}
    for r in db.all("SELECT exercise_id, class_id FROM exercise_classes"):
        links.setdefault(r["exercise_id"], []).append(r["class_id"])
    classes = my_classes(u)
    return {r["id"] for r in rows if can_manage_exercise(u, dict(r, class_ids=links.get(r["id"], [])), classes)}


def can_manage_student(u, s):
    return bool(s) and s["role"] == "student" and (is_admin(u) or (s["class_id"] in my_class_ids(u)))


def need_exercise(request, u, eid):
    ex = load_exercise(eid)
    if not ex or not can_manage_exercise(u, ex):
        flash(request, "Exercício não encontrado ou fora das suas turmas.", "error")
        raise Redirect("/teacher/exercises")
    return ex


def in_clause(ids):
    ids = list(ids) or [-1]
    return ",".join("?" * len(ids)), ids


# ---------- student-side helpers ----------

def is_past_due(ex):
    if not ex.get("due_date"):
        return False
    try:
        due = datetime.fromisoformat(ex["due_date"]).replace(tzinfo=TZ)
    except ValueError:
        return False
    return datetime.now(TZ) > due


def student_attempts(eid, sid):
    return db.all("SELECT * FROM attempts WHERE exercise_id=? AND student_id=? AND is_preview=0 ORDER BY id", (eid, sid))


def allowed_attempts(ex, sid):
    if ex["max_attempts"] == 0:
        return None
    g = db.one("SELECT extra FROM attempt_grants WHERE exercise_id=? AND student_id=?", (ex["id"], sid))
    return ex["max_attempts"] + (g["extra"] if g else 0)


def attempts_left(ex, sid, used):
    allowed = allowed_attempts(ex, sid)
    return None if allowed is None else max(0, allowed - used)


VISIBLE_SQL = """
SELECT e.* FROM exercises e
WHERE e.published=1 AND (
  EXISTS (SELECT 1 FROM exercise_classes ec WHERE ec.exercise_id=e.id AND ec.class_id=:cid)
  OR (NOT EXISTS (SELECT 1 FROM exercise_classes ec WHERE ec.exercise_id=e.id) AND e.level=:level)
)
"""


def visible_exercises(class_row):
    if not class_row:
        return []
    return db.all(VISIBLE_SQL + " ORDER BY e.level, e.subject, e.id DESC", {"cid": class_row["id"], "level": class_row["level"]})


def can_see(student, ex):
    if not student["class_id"]:
        return False
    cls = db.one("SELECT * FROM classes WHERE id=?", (student["class_id"],))
    return any(e["id"] == ex["id"] for e in visible_exercises(cls))


# ======================================================================
# auth & password recovery
# ======================================================================

_rate = {}


def rate_limited(key, limit, window):
    hits = [t for t in _rate.get(key, []) if t > time.time() - window]
    _rate[key] = hits
    return len(hits) >= limit


def hit(key):
    _rate.setdefault(key, []).append(time.time())


@app.get("/favicon.ico")
def favicon():
    return RedirectResponse("/static/img/favicon.png", 301)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    u = current_user(request)
    if not u:
        return RedirectResponse("/login", 303)
    return RedirectResponse("/student" if u["role"] == "student" else "/teacher", 303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if current_user(request):
        return RedirectResponse("/", 303)
    return render(request, "login.html")


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    key = "login:" + client_ip(request)
    if rate_limited(key, 10, 600):
        flash(request, "Muitas tentativas. Aguarde alguns minutos.", "error")
        return RedirectResponse("/login", 303)
    ident = username.strip()
    u = db.one("SELECT * FROM users WHERE active=1 AND (username=? OR (email IS NOT NULL AND email=?))", (ident, ident.lower()))
    if not u or not verify_password(password, u["password_hash"]):
        hit(key)
        flash(request, "Usuário ou senha incorretos.", "error")
        return RedirectResponse("/login", 303)
    _rate.pop(key, None)
    start_session(request, u)
    return RedirectResponse("/", 303)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", 303)


def create_reset_token(user_id, minutes):
    token = secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    db.run("INSERT INTO password_resets (token_hash, user_id, expires_at) VALUES (?,?,?)",
           (hashlib.sha256(token.encode()).hexdigest(), user_id, expires))
    return token


def reset_url(request, token):
    base = BASE_URL or str(request.base_url).rstrip("/")
    return f"{base}/reset/{token}"


def send_reset_email(user, url, minutes):
    hours = minutes // 60
    validity = f"{hours} hora(s)" if hours else f"{minutes} minutos"
    text = (f"Olá, {user['name']}!\n\nRecebemos um pedido para redefinir sua senha no {APP_NAME}.\n"
            f"Usuário: {user['username']}\n\nPara criar uma nova senha, acesse (válido por {validity}):\n{url}\n\n"
            f"Se você não pediu, ignore este e-mail — sua senha continua a mesma.\n\nLexWay English · {SCHOOL_EMAIL}")
    html = f"""<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;color:#062f34">
      <h2 style="font-family:Georgia,serif;color:#005555">Redefinição de senha</h2>
      <p>Olá, <b>{user['name']}</b>!</p><p>Recebemos um pedido para redefinir sua senha no <b>{APP_NAME}</b>.<br>
      Usuário: <b>{user['username']}</b></p>
      <p><a href="{url}" style="display:inline-block;background:#e31c79;color:#fff;padding:12px 22px;border-radius:10px;text-decoration:none;font-weight:bold">Criar nova senha</a></p>
      <p style="color:#777;font-size:13px">O link vale por {validity}. Se você não pediu, ignore este e-mail.</p>
      <p style="color:#777;font-size:13px">LexWay English · {SCHOOL_EMAIL}</p></div>"""
    return mailer.send(user["email"], f"{APP_NAME} — redefinição de senha", text, html)


@app.get("/forgot", response_class=HTMLResponse)
def forgot_page(request: Request):
    return render(request, "forgot.html")


@app.post("/forgot")
def forgot(request: Request, background: BackgroundTasks, identifier: str = Form(...)):
    key = "forgot:" + client_ip(request)
    if rate_limited(key, 5, 900):
        flash(request, "Muitos pedidos. Tente novamente em alguns minutos.", "error")
        return RedirectResponse("/forgot", 303)
    hit(key)
    ident = identifier.strip()
    u = db.one("SELECT * FROM users WHERE active=1 AND (username=? OR (email IS NOT NULL AND email=?))", (ident, ident.lower()))
    if u and u["email"]:
        token = create_reset_token(u["id"], RESET_MINUTES)
        background.add_task(send_reset_email, u, reset_url(request, token), RESET_MINUTES)
    elif u:
        logging.getLogger("worksheets").info("pedido de redefinição para '%s', que não tem e-mail cadastrado", u["username"])
    flash(request, "Se houver uma conta com e-mail cadastrado para esses dados, enviamos um link para criar uma nova senha. "
                   "Confira também a caixa de spam.")
    return RedirectResponse("/forgot?sent=1", 303)


def valid_reset(token):
    th = hashlib.sha256(token.encode()).hexdigest()
    r = db.one("""SELECT pr.*, u.name, u.username FROM password_resets pr JOIN users u ON u.id=pr.user_id
                  WHERE pr.token_hash=? AND pr.used_at IS NULL AND u.active=1""", (th,))
    if not r or r["expires_at"] < now_utc():
        return None
    return r


@app.get("/reset/{token}", response_class=HTMLResponse)
def reset_page(request: Request, token: str):
    r = valid_reset(token)
    return render(request, "reset.html", reset=r, token=token)


@app.post("/reset/{token}")
def reset_save(request: Request, token: str, new: str = Form(...), confirm: str = Form(...)):
    r = valid_reset(token)
    if not r:
        flash(request, "Link inválido ou expirado. Peça um novo.", "error")
        return RedirectResponse("/forgot", 303)
    if len(new) < 8 or new != confirm:
        flash(request, "A senha precisa ter pelo menos 8 caracteres e ser igual à confirmação.", "error")
        return RedirectResponse(f"/reset/{token}", 303)
    db.run("UPDATE users SET password_hash=? WHERE id=?", (hash_password(new), r["user_id"]))
    db.run("UPDATE password_resets SET used_at=? WHERE user_id=? AND used_at IS NULL", (now_utc(), r["user_id"]))
    request.session.clear()
    flash(request, f"Senha redefinida, {r['name']}! Entre com seu usuário ({r['username']}) e a nova senha.")
    return RedirectResponse("/login", 303)


@app.get("/account", response_class=HTMLResponse)
def account(request: Request):
    u = current_user(request)
    if not u:
        return RedirectResponse("/login", 303)
    return render(request, "account.html", u)


@app.post("/account/email")
def account_email(request: Request, email: str = Form("")):
    u = current_user(request)
    if not u:
        return RedirectResponse("/login", 303)
    try:
        e = clean_email(email)
        unique_or_error(u["username"], e, u["id"])
        db.run("UPDATE users SET email=? WHERE id=?", (e, u["id"]))
        flash(request, "E-mail atualizado.")
    except ValueError as ex:
        flash(request, str(ex), "error")
    return RedirectResponse("/account", 303)


@app.post("/account")
def account_save(request: Request, current: str = Form(...), new: str = Form(...), confirm: str = Form(...)):
    u = current_user(request)
    if not u:
        return RedirectResponse("/login", 303)
    if not verify_password(current, u["password_hash"]):
        flash(request, "Senha atual incorreta.", "error")
    elif len(new) < 8 or new != confirm:
        flash(request, "A nova senha precisa ter 8+ caracteres e ser igual à confirmação.", "error")
    else:
        db.run("UPDATE users SET password_hash=? WHERE id=?", (hash_password(new), u["id"]))
        start_session(request, db.one("SELECT * FROM users WHERE id=?", (u["id"],)))
        flash(request, "Senha alterada.")
    return RedirectResponse("/account", 303)


@app.post("/users/{uid}/reset-link", response_class=HTMLResponse)
def admin_reset_link(request: Request, uid: int, background: BackgroundTasks):
    """Staff generates a reset link for someone (e.g. a student without e-mail)."""
    u = need(request, *STAFF)
    target = db.one("SELECT * FROM users WHERE id=?", (uid,))
    if not target or not (is_admin(u) or can_manage_student(u, target)):
        flash(request, "Usuário fora do seu acesso.", "error")
        return RedirectResponse("/teacher", 303)
    token = create_reset_token(uid, RESET_ADMIN_HOURS * 60)
    url = reset_url(request, token)
    emailed = False
    if target["email"] and mailer.configured():
        background.add_task(send_reset_email, target, url, RESET_ADMIN_HOURS * 60)
        emailed = True
    return render(request, "reset_link.html", u, target=target, url=url, emailed=emailed, hours=RESET_ADMIN_HOURS)


# ======================================================================
# staff: dashboard
# ======================================================================

@app.get("/teacher", response_class=HTMLResponse)
def teacher_home(request: Request):
    u = need(request, *STAFF)
    classes = my_classes(u)
    marks, cids = in_clause(c["id"] for c in classes)
    scope = "" if is_admin(u) else f" AND s.class_id IN ({marks})"
    params = () if is_admin(u) else cids
    stats = {
        "classes": len(classes),
        "students": db.one(f"SELECT COUNT(*) n FROM users s WHERE s.role='student' AND s.active=1{scope}", params)["n"],
        "exercises": len(managed_exercise_ids(u)),
        "pending": db.one(f"SELECT COUNT(*) n FROM attempts a JOIN users s ON s.id=a.student_id WHERE a.needs_review=1 AND a.is_preview=0{scope}", params)["n"],
    }
    base = f"""SELECT a.*, s.name student, e.title FROM attempts a JOIN users s ON s.id=a.student_id
               JOIN exercises e ON e.id=a.exercise_id WHERE a.is_preview=0{scope}"""
    recent = db.all(base + " ORDER BY a.id DESC LIMIT 12", params)
    pending = db.all(base + " AND a.needs_review=1 ORDER BY a.id", params)
    return render(request, "teacher/dashboard.html", u, stats=stats, recent=recent, pending=pending, classes=classes)


# ======================================================================
# admin: classes & teachers
# ======================================================================

def teachers_all():
    return db.all("SELECT * FROM users WHERE role IN ('teacher','admin') ORDER BY role, name")


@app.get("/admin/classes", response_class=HTMLResponse)
def admin_classes(request: Request):
    u = need(request, "admin")
    rows = db.all("""SELECT c.*,
                       (SELECT COUNT(*) FROM users s WHERE s.class_id=c.id AND s.role='student' AND s.active=1) students,
                       (SELECT group_concat(t.name, ', ') FROM class_teachers ct JOIN users t ON t.id=ct.teacher_id WHERE ct.class_id=c.id) teacher_names
                     FROM classes c ORDER BY c.level, c.name""")
    for r in rows:
        r["teacher_ids"] = [x["teacher_id"] for x in db.all("SELECT teacher_id FROM class_teachers WHERE class_id=?", (r["id"],))]
    return render(request, "admin/classes.html", u, classes=rows, teachers=[t for t in teachers_all() if t["role"] == "teacher"])


@app.post("/admin/classes")
async def admin_class_save(request: Request):
    need(request, "admin")
    form = await request.form()
    name = str(form.get("name", "")).strip()
    level = str(form.get("level", ""))
    description = str(form.get("description", "")).strip()
    class_id = int(form.get("class_id") or 0)
    teacher_ids = [int(t) for t in form.getlist("teacher_ids")]
    if level not in grading.LEVELS or not name:
        flash(request, "Informe nome e nível válidos.", "error")
        return RedirectResponse("/admin/classes", 303)
    with db.conn() as c:
        if class_id:
            c.execute("UPDATE classes SET name=?, level=?, description=? WHERE id=?", (name, level, description, class_id))
        else:
            class_id = c.execute("INSERT INTO classes (name, level, description) VALUES (?,?,?)", (name, level, description)).lastrowid
        c.execute("DELETE FROM class_teachers WHERE class_id=?", (class_id,))
        for tid in teacher_ids:
            c.execute("INSERT OR IGNORE INTO class_teachers (class_id, teacher_id) SELECT ?, id FROM users WHERE id=? AND role='teacher'", (class_id, tid))
    flash(request, "Turma salva.")
    return RedirectResponse("/admin/classes", 303)


@app.post("/admin/classes/{cid}/delete")
def admin_class_delete(request: Request, cid: int):
    need(request, "admin")
    db.run("DELETE FROM classes WHERE id=?", (cid,))
    flash(request, "Turma excluída. Os alunos dela ficaram sem turma.")
    return RedirectResponse("/admin/classes", 303)


@app.get("/admin/teachers", response_class=HTMLResponse)
def admin_teachers(request: Request):
    u = need(request, "admin")
    rows = teachers_all()
    for t in rows:
        t["classes"] = db.all("""SELECT c.* FROM classes c JOIN class_teachers ct ON ct.class_id=c.id
                                 WHERE ct.teacher_id=? ORDER BY c.level, c.name""", (t["id"],))
        t["class_ids"] = [c["id"] for c in t["classes"]]
    return render(request, "admin/teachers.html", u, teachers=rows, classes=db.all("SELECT * FROM classes ORDER BY level, name"))


@app.post("/admin/teachers")
async def admin_teacher_save(request: Request):
    u = need(request, "admin")
    form = await request.form()
    tid = int(form.get("user_id") or 0)
    password = str(form.get("password", ""))
    role = form.get("role") if form.get("role") in ("teacher", "admin") else "teacher"
    active = 1 if str(form.get("active", "1")) == "1" else 0
    try:
        name = str(form.get("name", "")).strip()
        if not name:
            raise ValueError("Informe o nome.")
        username = clean_username(form.get("username"))
        email = clean_email(form.get("email"))
        unique_or_error(username, email, tid)
        if tid == u["id"] and (role != "admin" or not active):
            raise ValueError("Você não pode remover seu próprio acesso de administrador.")
        if (not tid or password) and len(password) < 8:
            raise ValueError("A senha precisa ter pelo menos 8 caracteres.")
        if tid and not db.one("SELECT id FROM users WHERE id=? AND role IN ('teacher','admin')", (tid,)):
            raise ValueError("Professor não encontrado.")
    except ValueError as e:
        flash(request, str(e), "error")
        return RedirectResponse("/admin/teachers", 303)
    class_ids = [int(c) for c in form.getlist("class_ids")]
    with db.conn() as c:
        if tid:
            c.execute("UPDATE users SET name=?, username=?, email=?, role=?, active=? WHERE id=?", (name, username, email, role, active, tid))
            if password:
                c.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_password(password), tid))
        else:
            tid = c.execute("INSERT INTO users (username, name, email, password_hash, role) VALUES (?,?,?,?,?)",
                            (username, name, email, hash_password(password), role)).lastrowid
        c.execute("DELETE FROM class_teachers WHERE teacher_id=?", (tid,))
        if role == "teacher":
            for cid in class_ids:
                c.execute("INSERT OR IGNORE INTO class_teachers (class_id, teacher_id) SELECT id, ? FROM classes WHERE id=?", (tid, cid))
    flash(request, f"{ROLES[role]} {name} salvo(a). Login: {username}")
    return RedirectResponse("/admin/teachers", 303)


# ======================================================================
# staff: classes (read-only view for teachers)
# ======================================================================

@app.get("/teacher/classes", response_class=HTMLResponse)
def teacher_classes(request: Request):
    u = need(request, *STAFF)
    if is_admin(u):
        return RedirectResponse("/admin/classes", 303)
    rows = my_classes(u)
    for r in rows:
        r["students"] = db.all("SELECT * FROM users WHERE role='student' AND active=1 AND class_id=? ORDER BY name", (r["id"],))
        r["teacher_names"] = ", ".join(t["name"] for t in db.all(
            "SELECT t.name FROM class_teachers ct JOIN users t ON t.id=ct.teacher_id WHERE ct.class_id=? ORDER BY t.name", (r["id"],)))
    return render(request, "teacher/my_classes.html", u, classes=rows)


# ======================================================================
# staff: students
# ======================================================================

@app.get("/teacher/students", response_class=HTMLResponse)
def students_page(request: Request, class_id: int = 0):
    u = need(request, *STAFF)
    classes = my_classes(u)
    ids = [c["id"] for c in classes]
    sql = """SELECT s.*, c.name class_name, c.level class_level,
               (SELECT COUNT(*) FROM attempts a WHERE a.student_id=s.id AND a.is_preview=0) attempts
             FROM users s LEFT JOIN classes c ON c.id=s.class_id WHERE s.role='student'"""
    params = []
    if class_id and class_id in ids:
        sql += " AND s.class_id=?"
        params.append(class_id)
    elif not is_admin(u):
        marks, p = in_clause(ids)
        sql += f" AND s.class_id IN ({marks})"
        params += p
    rows = db.all(sql + " ORDER BY s.active DESC, s.name", params)
    return render(request, "teacher/students.html", u, students=rows, classes=classes, class_id=class_id)


@app.post("/teacher/students")
async def student_save(request: Request):
    u = need(request, *STAFF)
    form = await request.form()
    sid = int(form.get("student_id") or 0)
    password = str(form.get("password", ""))
    cid = int(form.get("class_id") or 0) or None
    active = 1 if str(form.get("active", "1")) == "1" else 0
    try:
        name = str(form.get("name", "")).strip()
        if not name:
            raise ValueError("Informe o nome.")
        username = clean_username(form.get("username"))
        email = clean_email(form.get("email"))
        unique_or_error(username, email, sid)
        if not is_admin(u) and cid not in my_class_ids(u):
            raise ValueError("Escolha uma das suas turmas.")
        if sid:
            s = db.one("SELECT * FROM users WHERE id=?", (sid,))
            if not can_manage_student(u, s):
                raise ValueError("Aluno fora das suas turmas.")
        if (not sid or password) and len(password) < 6:
            raise ValueError("A senha do aluno precisa de pelo menos 6 caracteres.")
    except ValueError as e:
        flash(request, str(e), "error")
        return RedirectResponse("/teacher/students", 303)
    if sid:
        db.run("UPDATE users SET name=?, username=?, email=?, class_id=?, active=? WHERE id=? AND role='student'",
               (name, username, email, cid, active, sid))
        if password:
            db.run("UPDATE users SET password_hash=? WHERE id=?", (hash_password(password), sid))
        flash(request, "Aluno atualizado.")
    else:
        db.run("INSERT INTO users (username, name, email, password_hash, role, class_id) VALUES (?,?,?,?, 'student', ?)",
               (username, name, email, hash_password(password), cid))
        flash(request, f"Aluno criado. Login: {username}")
    return RedirectResponse("/teacher/students", 303)


@app.get("/teacher/students/{sid}", response_class=HTMLResponse)
def student_detail(request: Request, sid: int):
    u = need(request, *STAFF)
    s = db.one("SELECT s.*, c.name class_name FROM users s LEFT JOIN classes c ON c.id=s.class_id WHERE s.id=?", (sid,))
    if not can_manage_student(u, s):
        flash(request, "Aluno fora das suas turmas.", "error")
        raise Redirect("/teacher/students")
    attempts = db.all("""SELECT a.*, e.title, e.level, e.subject FROM attempts a JOIN exercises e ON e.id=a.exercise_id
                         WHERE a.student_id=? AND a.is_preview=0 ORDER BY a.id DESC""", (sid,))
    return render(request, "teacher/student_detail.html", u, s=s, attempts=attempts)


# ======================================================================
# staff: exercises
# ======================================================================

@app.get("/teacher/exercises", response_class=HTMLResponse)
def exercises_page(request: Request, level: str = "", subject: str = "", class_id: int = 0):
    u = need(request, *STAFF)
    marks, ids = in_clause(managed_exercise_ids(u))
    sql = f"""SELECT e.*, cu.name author,
               (SELECT COUNT(*) FROM attempts a WHERE a.exercise_id=e.id AND a.is_preview=0) attempts,
               (SELECT group_concat(c.name, ', ') FROM exercise_classes ec JOIN classes c ON c.id=ec.class_id WHERE ec.exercise_id=e.id) class_names
             FROM exercises e LEFT JOIN users cu ON cu.id=e.created_by WHERE e.id IN ({marks})"""
    params = list(ids)
    if level:
        sql += " AND e.level=?"
        params.append(level)
    if subject:
        sql += " AND e.subject=?"
        params.append(subject)
    if class_id:
        sql += " AND e.id IN (SELECT exercise_id FROM exercise_classes WHERE class_id=?)"
        params.append(class_id)
    rows = db.all(sql + " ORDER BY e.id DESC", params)
    for r in rows:
        r["n_items"] = len(json.loads(r["items"]))
    return render(request, "teacher/exercises.html", u, exercises=rows, classes=my_classes(u),
                  f={"level": level, "subject": subject, "class_id": class_id})


def _editor(request, u, ex):
    classes = my_classes(u)
    mine = {c["id"] for c in classes}
    other = [c["name"] for c in db.all("SELECT * FROM classes ORDER BY name") if c["id"] in ex["class_ids"] and c["id"] not in mine]
    return render(request, "teacher/exercise_form.html", u, ex=ex, classes=classes, other_classes=other)


@app.get("/teacher/exercises/new", response_class=HTMLResponse)
def exercise_new(request: Request):
    u = need(request, *STAFF)
    ex = {"id": 0, "title": "", "description": "", "subject": "Grammar", "topic": "", "level": "A1", "items": [],
          "max_attempts": 3, "grading": "best", "show_answers": "end", "published": 0, "due_date": "", "class_ids": []}
    return _editor(request, u, ex)


@app.get("/teacher/exercises/{eid}/edit", response_class=HTMLResponse)
def exercise_edit(request: Request, eid: int):
    u = need(request, *STAFF)
    return _editor(request, u, need_exercise(request, u, eid))


@app.post("/teacher/exercises/save")
async def exercise_save(request: Request):
    u = need(request, *STAFF)
    data = await request.json()
    eid = int(data.get("id") or 0)
    try:
        items = grading.validate_items(data.get("items"))
        title = str(data.get("title", "")).strip()[:200]
        if not title:
            raise ValueError("Dê um título ao exercício.")
        level = data.get("level")
        subject = data.get("subject")
        if level not in grading.LEVELS or subject not in grading.SUBJECTS:
            raise ValueError("Nível ou matéria inválidos.")
        gpolicy = data.get("grading") if data.get("grading") in grading.GRADING else "best"
        show = data.get("show_answers") if data.get("show_answers") in grading.SHOW_ANSWERS else "end"
        max_attempts = max(0, min(50, int(data.get("max_attempts") or 0)))
        due = str(data.get("due_date") or "").strip() or None
        if due:
            datetime.fromisoformat(due)
        requested = {int(c) for c in data.get("class_ids", [])}
        mine = my_class_ids(u)
        if not is_admin(u) and requested - mine:
            raise ValueError("Você só pode atribuir exercícios às suas turmas.")
        keep = set()
        if eid:
            existing = load_exercise(eid)
            if not existing or not can_manage_exercise(u, existing):
                raise ValueError("Exercício fora das suas turmas.")
            if not is_admin(u):
                keep = set(existing["class_ids"]) - mine  # assignments to other teachers' classes stay untouched
        final_classes = requested | keep
        if not is_admin(u) and not final_classes:
            raise ValueError("Selecione pelo menos uma das suas turmas.")
    except (ValueError, TypeError) as e:
        return JSONResponse({"error": str(e) if str(e) else "Dados inválidos."}, status_code=400)

    values = (title, str(data.get("description", "")).strip()[:3000], subject, str(data.get("topic", "")).strip()[:120],
              level, json.dumps(items, ensure_ascii=False), max_attempts, gpolicy, show, 1 if data.get("published") else 0, due)
    with db.conn() as c:
        if eid:
            c.execute("""UPDATE exercises SET title=?, description=?, subject=?, topic=?, level=?, items=?, max_attempts=?,
                         grading=?, show_answers=?, published=?, due_date=?, updated_at=CURRENT_TIMESTAMP WHERE id=?""", values + (eid,))
        else:
            eid = c.execute("""INSERT INTO exercises (title, description, subject, topic, level, items, max_attempts, grading,
                               show_answers, published, due_date, created_by) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", values + (u["id"],)).lastrowid
        c.execute("DELETE FROM exercise_classes WHERE exercise_id=?", (eid,))
        for cid in final_classes:
            c.execute("INSERT OR IGNORE INTO exercise_classes SELECT ?, id FROM classes WHERE id=?", (eid, cid))
    flash(request, "Exercício salvo.")
    return {"id": eid, "redirect": f"/teacher/exercises/{eid}/edit"}


@app.post("/teacher/exercises/{eid}/duplicate")
def exercise_duplicate(request: Request, eid: int):
    u = need(request, *STAFF)
    ex = need_exercise(request, u, eid)
    with db.conn() as c:
        new = c.execute("""INSERT INTO exercises (title, description, subject, topic, level, items, max_attempts, grading, show_answers,
                           published, due_date, created_by) VALUES (?,?,?,?,?,?,?,?,?,0,?,?)""",
                        (ex["title"] + " (cópia)", ex["description"], ex["subject"], ex["topic"], ex["level"],
                         json.dumps(ex["items"], ensure_ascii=False), ex["max_attempts"], ex["grading"], ex["show_answers"],
                         ex["due_date"], u["id"])).lastrowid
        mine = my_class_ids(u)
        for cid in ex["class_ids"]:
            if is_admin(u) or cid in mine:
                c.execute("INSERT INTO exercise_classes VALUES (?,?)", (new, cid))
    flash(request, "Cópia criada (não publicada).")
    return RedirectResponse(f"/teacher/exercises/{new}/edit", 303)


@app.post("/teacher/exercises/{eid}/toggle")
def exercise_toggle(request: Request, eid: int):
    u = need(request, *STAFF)
    need_exercise(request, u, eid)
    db.run("UPDATE exercises SET published=1-published WHERE id=?", (eid,))
    return RedirectResponse("/teacher/exercises", 303)


@app.post("/teacher/exercises/{eid}/delete")
def exercise_delete(request: Request, eid: int):
    u = need(request, *STAFF)
    need_exercise(request, u, eid)
    db.run("DELETE FROM exercises WHERE id=?", (eid,))
    flash(request, "Exercício excluído.")
    return RedirectResponse("/teacher/exercises", 303)


@app.get("/teacher/exercises/{eid}/preview", response_class=HTMLResponse)
def exercise_preview(request: Request, eid: int):
    u = need(request, *STAFF)
    ex = need_exercise(request, u, eid)
    payload = {"items": [grading.student_item(i) for i in ex["items"]], "submitUrl": f"/teacher/exercises/{eid}/preview"}
    return render(request, "player.html", u, ex=ex, payload=payload, preview=True, left=None, used=0)


@app.post("/teacher/exercises/{eid}/preview")
async def exercise_preview_submit(request: Request, eid: int):
    u = need(request, *STAFF)
    ex = load_exercise(eid)
    if not ex or not can_manage_exercise(u, ex):
        return JSONResponse({"error": "Exercício não encontrado"}, status_code=404)
    answers = (await request.json()).get("answers", {})
    res = grading.grade_exercise(ex["items"], answers)
    aid = db.run("""INSERT INTO attempts (exercise_id, student_id, items_snapshot, answers, results, score, max_score, needs_review, is_preview)
                    VALUES (?,?,?,?,?,?,?,0,1)""", (eid, u["id"], json.dumps(ex["items"], ensure_ascii=False),
                                                   json.dumps(answers, ensure_ascii=False), json.dumps(res, ensure_ascii=False),
                                                   res["score"], res["max_score"]))
    return {"redirect": f"/teacher/attempts/{aid}"}


@app.get("/teacher/exercises/{eid}/results", response_class=HTMLResponse)
def exercise_results(request: Request, eid: int):
    u = need(request, *STAFF)
    ex = need_exercise(request, u, eid)
    scope_ids = None if is_admin(u) else my_class_ids(u)
    if ex["class_ids"]:
        target = [c for c in ex["class_ids"] if scope_ids is None or c in scope_ids]
        marks, p = in_clause(target)
        students = db.all(f"""SELECT s.*, c.name class_name FROM users s JOIN classes c ON c.id=s.class_id
                              WHERE s.role='student' AND s.active=1 AND s.class_id IN ({marks}) ORDER BY c.name, s.name""", p)
    else:
        students = [s for s in db.all("""SELECT s.*, c.name class_name FROM users s JOIN classes c ON c.id=s.class_id
                                         WHERE s.role='student' AND s.active=1 AND c.level=? ORDER BY c.name, s.name""", (ex["level"],))
                    if scope_ids is None or s["class_id"] in scope_ids]
    rows = []
    for s in students:
        att = student_attempts(eid, s["id"])
        rows.append({"s": s, "attempts": att, "final": grading.final_grade(att, ex["grading"]),
                     "allowed": allowed_attempts(ex, s["id"]), "pending": any(a["needs_review"] for a in att)})
    return render(request, "teacher/results.html", u, ex=ex, rows=rows)


@app.post("/teacher/exercises/{eid}/grant")
def grant_attempt(request: Request, eid: int, student_id: int = Form(...)):
    u = need(request, *STAFF)
    need_exercise(request, u, eid)
    if not can_manage_student(u, db.one("SELECT * FROM users WHERE id=?", (student_id,))):
        flash(request, "Aluno fora das suas turmas.", "error")
    else:
        db.run("""INSERT INTO attempt_grants (exercise_id, student_id, extra) VALUES (?,?,1)
                  ON CONFLICT(exercise_id, student_id) DO UPDATE SET extra=extra+1""", (eid, student_id))
        flash(request, "Tentativa extra liberada.")
    return RedirectResponse(f"/teacher/exercises/{eid}/results", 303)


# ======================================================================
# staff: attempts & review
# ======================================================================

def attempt_context(a):
    a["items"] = json.loads(a["items_snapshot"])
    a["res"] = json.loads(a["results"])
    a["res_by_id"] = {r["id"]: r for r in a["res"]["items"]}
    return a


def staff_attempt(request, u, aid):
    a = db.one("""SELECT a.*, s.name student, e.title, e.level, e.subject, e.id eid, e.show_answers FROM attempts a
                  JOIN users s ON s.id=a.student_id JOIN exercises e ON e.id=a.exercise_id WHERE a.id=?""", (aid,))
    if not a:
        raise Redirect("/teacher")
    if not (is_admin(u) or a["student_id"] == u["id"] or can_manage_student(u, db.one("SELECT * FROM users WHERE id=?", (a["student_id"],)))):
        flash(request, "Envio fora das suas turmas.", "error")
        raise Redirect("/teacher")
    return a


@app.get("/teacher/attempts/{aid}", response_class=HTMLResponse)
def attempt_view(request: Request, aid: int):
    u = need(request, *STAFF)
    a = staff_attempt(request, u, aid)
    return render(request, "result.html", u, a=attempt_context(a), reveal=True, teacher=True, left=None)


@app.post("/teacher/attempts/{aid}/review")
async def attempt_review(request: Request, aid: int):
    u = need(request, *STAFF)
    a = staff_attempt(request, u, aid)
    form = await request.form()
    res = json.loads(a["results"])
    for r in res["items"]:
        key = f"score_{r['id']}"
        if key in form and str(form[key]).strip() != "":
            try:
                r["score"] = round(max(0.0, min(r["points"], float(str(form[key]).replace(",", ".")))), 2)
            except ValueError:
                continue
            r["needs_review"] = False
            r["reviewed"] = True
    res["score"] = round(sum(r["score"] for r in res["items"]), 2)
    res["needs_review"] = any(r["needs_review"] for r in res["items"])
    db.run("UPDATE attempts SET results=?, score=?, needs_review=?, feedback=?, reviewed_at=? WHERE id=?",
           (json.dumps(res, ensure_ascii=False), res["score"], 1 if res["needs_review"] else 0,
            str(form.get("feedback", "")).strip()[:3000], now_utc(), aid))
    flash(request, "Correção salva.")
    return RedirectResponse(f"/teacher/attempts/{aid}", 303)


# ======================================================================
# staff: gradebook
# ======================================================================

def gradebook_data(cls):
    exercises = visible_exercises(cls)
    students = db.all("SELECT * FROM users WHERE role='student' AND active=1 AND class_id=? ORDER BY name", (cls["id"],))
    rows = []
    for s in students:
        cells, grades = [], []
        for e in exercises:
            att = student_attempts(e["id"], s["id"])
            g = grading.final_grade(att, e["grading"])
            cells.append({"grade": g, "n": len(att), "pending": any(a["needs_review"] for a in att)})
            if g is not None:
                grades.append(g)
        rows.append({"s": s, "cells": cells, "avg": round(sum(grades) / len(grades), 1) if grades else None, "done": len(grades)})
    return exercises, rows


@app.get("/teacher/gradebook", response_class=HTMLResponse)
def gradebook(request: Request, class_id: int = 0):
    u = need(request, *STAFF)
    classes = my_classes(u)
    cls = next((c for c in classes if c["id"] == class_id), classes[0] if classes else None)
    exercises, rows = gradebook_data(cls) if cls else ([], [])
    return render(request, "teacher/gradebook.html", u, classes=classes, cls=cls, exercises=exercises, rows=rows)


@app.get("/teacher/gradebook.csv")
def gradebook_csv(request: Request, class_id: int):
    u = need(request, *STAFF)
    cls = next((c for c in my_classes(u) if c["id"] == class_id), None)
    if not cls:
        raise Redirect("/teacher/gradebook")
    exercises, rows = gradebook_data(cls)
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";")
    w.writerow(["Aluno", "Usuário"] + [e["title"] for e in exercises] + ["Média"])
    for r in rows:
        w.writerow([r["s"]["name"], r["s"]["username"]] + [fmt_grade(c["grade"]) for c in r["cells"]] + [fmt_grade(r["avg"])])
    slug = re.sub(r"[^A-Za-z0-9]+", "-", unicodedata.normalize("NFKD", cls["name"]).encode("ascii", "ignore").decode()).strip("-")
    return Response("﻿" + buf.getvalue(), media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="notas-{slug or "turma"}.csv"'})


# ======================================================================
# student
# ======================================================================

@app.get("/student", response_class=HTMLResponse)
def student_home(request: Request, subject: str = ""):
    u = need(request, "student")
    cls = db.one("SELECT * FROM classes WHERE id=?", (u["class_id"],)) if u["class_id"] else None
    todo, done = [], []
    for e in visible_exercises(cls):
        if subject and e["subject"] != subject:
            continue
        att = student_attempts(e["id"], u["id"])
        e["n_items"] = len(json.loads(e["items"]))
        e["used"] = len(att)
        e["left"] = attempts_left(e, u["id"], len(att))
        e["final"] = grading.final_grade(att, e["grading"])
        e["pending"] = any(a["needs_review"] for a in att)
        e["last_attempt"] = att[-1]["id"] if att else None
        e["past_due"] = is_past_due(e)
        (done if att else todo).append(e)
    return render(request, "student/home.html", u, cls=cls, todo=todo, done=done, subject=subject)


@app.get("/student/exercises/{eid}", response_class=HTMLResponse)
def student_exercise(request: Request, eid: int):
    u = need(request, "student")
    ex = load_exercise(eid)
    if not ex or not can_see(u, ex):
        flash(request, "Exercício indisponível.", "error")
        raise Redirect("/student")
    used = len(student_attempts(eid, u["id"]))
    left = attempts_left(ex, u["id"], used)
    if left == 0 or is_past_due(ex):
        flash(request, "Você não tem mais tentativas neste exercício." if left == 0 else "O prazo deste exercício acabou.", "error")
        raise Redirect("/student")
    payload = {"items": [grading.student_item(i) for i in ex["items"]], "submitUrl": f"/student/exercises/{eid}/submit"}
    return render(request, "player.html", u, ex=ex, payload=payload, preview=False, left=left, used=used)


@app.post("/student/exercises/{eid}/submit")
async def student_submit(request: Request, eid: int):
    u = need(request, "student")
    ex = load_exercise(eid)
    if not ex or not can_see(u, ex):
        return JSONResponse({"error": "Exercício indisponível."}, status_code=404)
    used = len(student_attempts(eid, u["id"]))
    if attempts_left(ex, u["id"], used) == 0 or is_past_due(ex):
        return JSONResponse({"error": "Sem tentativas disponíveis ou prazo encerrado."}, status_code=403)
    answers = (await request.json()).get("answers", {})
    res = grading.grade_exercise(ex["items"], answers)
    aid = db.run("""INSERT INTO attempts (exercise_id, student_id, items_snapshot, answers, results, score, max_score, needs_review)
                    VALUES (?,?,?,?,?,?,?,?)""", (eid, u["id"], json.dumps(ex["items"], ensure_ascii=False),
                                                 json.dumps(answers, ensure_ascii=False), json.dumps(res, ensure_ascii=False),
                                                 res["score"], res["max_score"], 1 if res["needs_review"] else 0))
    return {"redirect": f"/student/attempts/{aid}"}


@app.get("/student/attempts/{aid}", response_class=HTMLResponse)
def student_attempt(request: Request, aid: int):
    u = need(request, "student")
    a = db.one("""SELECT a.*, e.title, e.level, e.subject, e.id eid, e.show_answers, e.max_attempts, e.grading, e.due_date
                  FROM attempts a JOIN exercises e ON e.id=a.exercise_id WHERE a.id=? AND a.student_id=? AND a.is_preview=0""", (aid, u["id"]))
    if not a:
        raise Redirect("/student")
    ex = {"id": a["eid"], "max_attempts": a["max_attempts"], "due_date": a["due_date"]}
    used = len(student_attempts(a["eid"], u["id"]))
    left = attempts_left(ex, u["id"], used)
    if is_past_due(ex):
        left = 0
    reveal = a["show_answers"] == "always" or (a["show_answers"] == "end" and left == 0)
    return render(request, "result.html", u, a=attempt_context(a), reveal=reveal, teacher=False, left=left, used=used)


@app.get("/student/grades", response_class=HTMLResponse)
def student_grades(request: Request):
    u = need(request, "student")
    cls = db.one("SELECT * FROM classes WHERE id=?", (u["class_id"],)) if u["class_id"] else None
    rows, grades = [], []
    for e in visible_exercises(cls):
        att = student_attempts(e["id"], u["id"])
        g = grading.final_grade(att, e["grading"])
        rows.append({"e": e, "attempts": att, "final": g, "pending": any(a["needs_review"] for a in att)})
        if g is not None:
            grades.append(g)
    avg = round(sum(grades) / len(grades), 1) if grades else None
    return render(request, "student/grades.html", u, cls=cls, rows=rows, avg=avg)
