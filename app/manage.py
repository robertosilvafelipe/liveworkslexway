"""Command-line administration.

  python -m app.manage create-admin --username lexwayenglish --name "LexWay English" --email lexway.english@gmail.com
  python -m app.manage set-password --username lisa
  python -m app.manage link-teacher --username lisa --class-name "A1 — Turma da Lisa"
  python -m app.manage test-email --to alguem@exemplo.com

Passwords are read from the terminal (or from --password, for scripts).
"""
import argparse
import getpass
import sys

from . import db, mailer
from .auth import hash_password


def ask_password(given):
    if given:
        return given
    pw = getpass.getpass("Senha (mín. 8): ")
    if pw != getpass.getpass("Confirme: "):
        sys.exit("As senhas não conferem.")
    return pw


def main():
    ap = argparse.ArgumentParser(prog="python -m app.manage")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("create-admin")
    a.add_argument("--username", required=True)
    a.add_argument("--name", required=True)
    a.add_argument("--email", default=None)
    a.add_argument("--password")
    p = sub.add_parser("set-password")
    p.add_argument("--username", required=True)
    p.add_argument("--password")
    l = sub.add_parser("link-teacher")
    l.add_argument("--username", required=True)
    l.add_argument("--class-name", required=True)
    t = sub.add_parser("test-email")
    t.add_argument("--to", required=True)
    args = ap.parse_args()
    db.init()

    if args.cmd == "create-admin":
        if db.one("SELECT id FROM users WHERE username=?", (args.username,)):
            sys.exit(f"Usuário {args.username} já existe.")
        pw = ask_password(args.password)
        if len(pw) < 8:
            sys.exit("Senha curta (mín. 8).")
        db.run("INSERT INTO users (username, name, email, password_hash, role) VALUES (?,?,?,?, 'admin')",
               (args.username.lower(), args.name, (args.email or "").lower() or None, hash_password(pw)))
        print(f"Administrador {args.username} criado.")
    elif args.cmd == "set-password":
        u = db.one("SELECT id FROM users WHERE username=?", (args.username,))
        if not u:
            sys.exit("Usuário não encontrado.")
        db.run("UPDATE users SET password_hash=? WHERE id=?", (hash_password(ask_password(args.password)), u["id"]))
        print("Senha alterada.")
    elif args.cmd == "link-teacher":
        u = db.one("SELECT id FROM users WHERE username=? AND role='teacher'", (args.username,))
        c = db.one("SELECT id FROM classes WHERE name=?", (args.class_name,))
        if not u or not c:
            sys.exit("Professor(a) ou turma não encontrados.")
        db.run("INSERT OR IGNORE INTO class_teachers (class_id, teacher_id) VALUES (?,?)", (c["id"], u["id"]))
        print("Vinculado.")
    elif args.cmd == "test-email":
        ok = mailer.send(args.to, "Teste de e-mail — LexWay Worksheets", "Se você recebeu esta mensagem, o SMTP está funcionando.")
        print("Enviado." if ok else "Falhou (veja o log / configuração WS_SMTP_*).")


if __name__ == "__main__":
    main()
