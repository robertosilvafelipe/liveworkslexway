"""Exercise item types: validation, student-safe views and automatic correction."""
import random
import re
import secrets
import unicodedata

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
SUBJECTS = ["Grammar", "Vocabulary", "Reading", "Writing", "Listening", "Speaking", "Video"]
TYPES = {
    "fill": "Preencher lacunas",
    "dropdown": "Escolher na lista (dropdown)",
    "choice": "Múltipla escolha",
    "truefalse": "Verdadeiro ou falso",
    "order": "Colocar na ordem",
    "match": "Ligar colunas",
    "group": "Classificar em grupos",
    "free": "Texto livre",
    "speak": "Falar (gravar a voz)",
    "info": "Texto de leitura / instruções (sem pontos)",
    "video": "Vídeo interativo (pausa com perguntas)",
}
GRADING = {"best": "Melhor tentativa", "last": "Última tentativa", "average": "Média das tentativas"}
SHOW_ANSWERS = {
    "always": "Sempre, após cada envio",
    "end": "Só quando acabarem as tentativas",
    "never": "Nunca (só mostra certo/errado)",
}

BLANK_RE = re.compile(r"\[([^\[\]]+)\]")


def norm(s) -> str:
    s = unicodedata.normalize("NFKC", str(s if s is not None else ""))
    s = s.replace("’", "'").replace("‘", "'").replace("`", "'").replace("´", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def norm_loose(s) -> str:
    return re.sub(r"\s*([.!?,;:])\s*$", "", norm(s)).strip()


# ---------- parsing helpers ----------

def parse_text(text: str):
    """Split a text with [blanks] into parts: ("t", str) or ("b", index, raw)."""
    parts, pos, idx = [], 0, 0
    for m in BLANK_RE.finditer(text or ""):
        if m.start() > pos:
            parts.append(("t", text[pos:m.start()]))
        parts.append(("b", idx, m.group(1)))
        idx += 1
        pos = m.end()
    if pos < len(text or ""):
        parts.append(("t", text[pos:]))
    return parts


def fill_answers(raw: str):
    return [a.strip() for a in raw.split("|") if a.strip()]


def dropdown_options(raw: str):
    opts = [o.strip() for o in raw.split("|") if o.strip()]
    correct = [o.lstrip("*").strip() for o in opts if o.startswith("*")]
    clean = [o.lstrip("*").strip() for o in opts]
    return clean, (correct or clean[:1])


def units(item) -> int:
    t = item["type"]
    if t in ("fill", "dropdown"):
        return len([p for p in parse_text(item.get("text", "")) if p[0] == "b"])
    if t == "truefalse":
        return len(item.get("statements", []))
    if t == "match":
        return len(item.get("pairs", []))
    if t == "group":
        return len(item.get("words", []))
    if t == "speak":
        return len(item.get("phrases", []))
    if t == "video":
        return len(item.get("stops", []))
    if t == "info":
        return 0
    return 1


def item_points(item) -> float:
    if item["type"] == "info":
        return 0.0
    p = item.get("points")
    try:
        if p not in (None, "") and float(p) > 0:
            return float(p)
    except (TypeError, ValueError):
        pass
    return 5.0 if item["type"] == "free" else float(max(units(item), 1))


# ---------- validation (teacher builder) ----------

def _s(v, maxlen=5000):
    return str(v if v is not None else "").strip()[:maxlen]


def validate_items(items):
    if not isinstance(items, list) or not items:
        raise ValueError("O exercício precisa de pelo menos uma questão.")
    clean, seen = [], set()
    for n, it in enumerate(items, 1):
        if not isinstance(it, dict) or it.get("type") not in TYPES:
            raise ValueError(f"Questão {n}: tipo inválido.")
        t = it["type"]
        iid = _s(it.get("id"), 40) or "i" + secrets.token_hex(4)
        while iid in seen:
            iid = "i" + secrets.token_hex(4)
        seen.add(iid)
        c = {"id": iid, "type": t, "prompt": _s(it.get("prompt"), 3000), "image": _s(it.get("image"), 500)}
        for k in ("translation", "example"):  # Portuguese translation of the command / worked example
            if _s(it.get(k)):
                c[k] = _s(it.get(k), 3000)
        if c["image"] and not re.match(r"^https?://", c["image"]):
            raise ValueError(f"Questão {n}: a imagem precisa ser um link http(s).")
        audio = _s(it.get("audio"), 500)
        if audio:
            if not re.match(r"^(https?://|/static/audio/)", audio):
                raise ValueError(f"Questão {n}: o áudio precisa ser um link http(s).")
            c["audio"] = audio
        if it.get("points") not in (None, ""):
            try:
                c["points"] = max(0.5, min(100.0, float(it["points"])))
            except (TypeError, ValueError):
                raise ValueError(f"Questão {n}: pontuação inválida.")

        if t in ("fill", "dropdown"):
            c["text"] = _s(it.get("text"), 8000)
            blanks = [p for p in parse_text(c["text"]) if p[0] == "b"]
            if not blanks:
                raise ValueError(f"Questão {n}: coloque as respostas entre [colchetes] no texto.")
            if t == "dropdown":
                for b in blanks:
                    opts, _ = dropdown_options(b[2])
                    if len(opts) < 2:
                        raise ValueError(f"Questão {n}: cada lista precisa de 2+ opções, ex.: [*am|is|are].")
        elif t == "choice":
            opts = [_s(o, 500) for o in it.get("options", []) if _s(o, 500)]
            if len(opts) < 2:
                raise ValueError(f"Questão {n}: informe pelo menos 2 alternativas.")
            try:
                correct = int(it.get("correct", 0))
            except (TypeError, ValueError):
                correct = 0
            if not 0 <= correct < len(opts):
                raise ValueError(f"Questão {n}: marque a alternativa correta.")
            c.update(options=opts, correct=correct)
        elif t == "truefalse":
            sts = [{"text": _s(s.get("text"), 500), "answer": bool(s.get("answer"))}
                   | ({"translation": _s(s.get("translation"), 500)} if _s(s.get("translation")) else {})
                   for s in it.get("statements", []) if isinstance(s, dict) and _s(s.get("text"))]
            if not sts:
                raise ValueError(f"Questão {n}: adicione afirmações.")
            c["statements"] = sts
        elif t == "order":
            tokens = [_s(x, 200) for x in it.get("tokens", []) if _s(x, 200)]
            if len(tokens) < 2:
                raise ValueError(f"Questão {n}: separe a frase em pelo menos 2 partes.")
            c["tokens"] = tokens
            c["alternatives"] = [_s(a, 1000) for a in it.get("alternatives", []) if _s(a, 1000)]
        elif t == "match":
            pairs = [{"left": _s(p.get("left"), 300), "right": _s(p.get("right"), 300)}
                     | ({"image": _s(p.get("image"), 500)} if _s(p.get("image")) else {})
                     for p in it.get("pairs", []) if isinstance(p, dict) and _s(p.get("left")) and _s(p.get("right"))]
            if len(pairs) < 2:
                raise ValueError(f"Questão {n}: adicione pelo menos 2 pares.")
            for p in pairs:  # optional picture shown to the student in place of the right-hand text
                if p.get("image") and not re.match(r"^(https?://|/static/img/)", p["image"]):
                    raise ValueError(f"Questão {n}: a figura do par precisa ser um link http(s).")
            c["pairs"] = pairs
        elif t == "group":
            cats = [_s(x, 100) for x in it.get("categories", []) if _s(x, 100)]
            words = [{"text": _s(w.get("text"), 200), "category": _s(w.get("category"), 100)}
                     for w in it.get("words", []) if isinstance(w, dict) and _s(w.get("text"))]
            if len(cats) < 2 or not words:
                raise ValueError(f"Questão {n}: informe 2+ grupos e as palavras.")
            for w in words:
                if w["category"] not in cats:
                    raise ValueError(f"Questão {n}: '{w['text']}' está num grupo que não existe.")
            c.update(categories=cats, words=words)
        elif t == "free":
            c["model_answer"] = _s(it.get("model_answer"), 5000)
            c["keywords"] = [_s(k, 100) for k in it.get("keywords", []) if _s(k, 100)]
            try:
                c["min_words"] = max(0, int(it.get("min_words") or 0))
            except (TypeError, ValueError):
                c["min_words"] = 0
        elif t == "speak":
            phrases = []
            for p in it.get("phrases", []):
                if not isinstance(p, dict) or not _s(p.get("text"), 300):
                    continue
                audio = _s(p.get("audio"), 500)
                if audio and not re.match(r"^(https?://|/static/audio/)", audio):
                    raise ValueError(f"Questão {n}: o áudio modelo precisa ser um link http(s).")
                phrases.append({"text": _s(p.get("text"), 300), "audio": audio})
            if not phrases:
                raise ValueError(f"Questão {n}: adicione as palavras ou frases que o aluno vai falar.")
            c["phrases"] = phrases
        elif t == "video":
            for k in ("video", "subtitles", "poster"):
                v = _s(it.get(k), 500)
                if v and not re.match(r"^(https?://|/static/video/)", v):
                    raise ValueError(f"Questão {n}: o vídeo precisa ser um link http(s).")
                if v:
                    c[k] = v
            if not c.get("video"):
                raise ValueError(f"Questão {n}: informe o link do vídeo.")
            stops = []
            for s in it.get("stops", []):
                opts = [_s(o, 300) for o in (s.get("options") or []) if _s(o, 300)] if isinstance(s, dict) else []
                if len(opts) < 2 or not _s(s.get("question")):
                    continue
                try:
                    at, correct = max(0.0, float(s.get("at", 0))), int(s.get("correct", 0))
                except (TypeError, ValueError):
                    raise ValueError(f"Questão {n}: pausa com tempo ou resposta inválida.")
                if not 0 <= correct < len(opts):
                    raise ValueError(f"Questão {n}: marque a alternativa correta de cada pausa.")
                stops.append({"at": at, "question": _s(s.get("question"), 500), "options": opts, "correct": correct}
                             | ({"translation": _s(s.get("translation"), 500)} if _s(s.get("translation")) else {}))
            if not stops:
                raise ValueError(f"Questão {n}: adicione as perguntas das pausas do vídeo.")
            c["stops"] = sorted(stops, key=lambda s: s["at"])
        elif t == "info":
            c["text"] = _s(it.get("text"), 8000)
            c.pop("points", None)
            if not c["text"] and not c["prompt"]:
                raise ValueError(f"Questão {n}: escreva o texto.")
        if not c["prompt"] and t in ("choice", "free"):
            raise ValueError(f"Questão {n}: escreva o enunciado.")
        clean.append(c)
    return clean


# ---------- student view (never contains the answers) ----------

def _shuffled(seq, avoid=None):
    seq = list(seq)
    for _ in range(8):
        random.shuffle(seq)
        if avoid is None or len(seq) < 2 or seq != list(avoid):
            break
    return seq


def student_item(item):
    t = item["type"]
    v = {"id": item["id"], "type": t, "prompt": item.get("prompt", ""), "image": item.get("image", ""),
         "audio": item.get("audio", ""), "points": item_points(item),
         "translation": item.get("translation", ""), "example": item.get("example", "")}
    if t in ("fill", "dropdown"):
        parts = []
        for p in parse_text(item["text"]):
            if p[0] == "t":
                parts.append({"t": p[1]})
            elif t == "fill":
                longest = max((len(a) for a in fill_answers(p[2])), default=6)
                parts.append({"b": p[1], "size": max(6, min(30, longest + 3))})
            else:
                parts.append({"b": p[1], "options": dropdown_options(p[2])[0]})
        v["parts"] = parts
    elif t == "choice":
        v["options"] = item["options"]
    elif t == "truefalse":
        v["statements"] = [s["text"] for s in item["statements"]]
        v["statement_translations"] = [s.get("translation", "") for s in item["statements"]]
    elif t == "order":
        v["tokens"] = _shuffled(item["tokens"], avoid=item["tokens"])
    elif t == "match":
        v["left"] = [p["left"] for p in item["pairs"]]
        rights = [p["right"] for p in item["pairs"]]
        v["right"] = _shuffled(rights, avoid=rights)
        images = {p["right"]: p["image"] for p in item["pairs"] if p.get("image")}
        if images:
            v["right_images"] = [images.get(r, "") for r in v["right"]]
    elif t == "group":
        v["categories"] = item["categories"]
        v["words"] = _shuffled([w["text"] for w in item["words"]])
    elif t == "free":
        v["min_words"] = item.get("min_words", 0)
    elif t == "speak":
        v["phrases"] = item["phrases"]
    elif t == "info":
        v["text"] = item.get("text", "")
    elif t == "video":
        v.update(video=item["video"], subtitles=item.get("subtitles", ""), poster=item.get("poster", ""),
                 stops=[{"at": s["at"], "question": s["question"], "translation": s.get("translation", ""),
                         "options": s["options"]} for s in item["stops"]])
    return v


# ---------- correction ----------

def grade_item(item, answer):
    t = item["type"]
    details, ok_units, n_units, needs_review = [], 0.0, units(item), False

    if t in ("fill", "dropdown"):
        given = answer if isinstance(answer, list) else []
        for p in parse_text(item["text"]):
            if p[0] != "b":
                continue
            g = given[p[1]] if p[1] < len(given) and given[p[1]] is not None else ""
            if t == "fill":
                expected = fill_answers(p[2])
                ok = norm_loose(g) != "" and norm_loose(g) in {norm_loose(a) for a in expected}
            else:
                _, expected = dropdown_options(p[2])
                ok = norm(g) in {norm(a) for a in expected}
            ok_units += ok
            details.append({"given": str(g), "expected": expected[0] if expected else "", "ok": ok})
    elif t == "choice":
        try:
            g = int(answer)
        except (TypeError, ValueError):
            g = None
        ok = g == item["correct"]
        ok_units += ok
        details.append({"given": item["options"][g] if g is not None and 0 <= g < len(item["options"]) else "",
                        "expected": item["options"][item["correct"]], "ok": ok, "given_index": g})
    elif t == "truefalse":
        given = answer if isinstance(answer, list) else []
        for i, s in enumerate(item["statements"]):
            g = given[i] if i < len(given) else None
            ok = isinstance(g, bool) and g == s["answer"]
            ok_units += ok
            details.append({"statement": s["text"], "translation": s.get("translation", ""), "given": g,
                            "expected": s["answer"], "ok": ok})
    elif t == "order":
        given = [str(x) for x in answer] if isinstance(answer, list) else []
        sentence = " ".join(given)
        valid = {norm_loose(" ".join(item["tokens"]))} | {norm_loose(a) for a in item.get("alternatives", [])}
        ok = len(given) == len(item["tokens"]) and norm_loose(sentence) in valid
        ok_units += ok
        details.append({"given": sentence, "expected": " ".join(item["tokens"]), "ok": ok})
    elif t == "match":
        given = answer if isinstance(answer, list) else []
        images = {norm(p["right"]): p.get("image", "") for p in item["pairs"]}
        for i, p in enumerate(item["pairs"]):
            g = given[i] if i < len(given) and given[i] is not None else ""
            ok = norm(g) == norm(p["right"])
            ok_units += ok
            details.append({"left": p["left"], "given": str(g), "expected": p["right"], "ok": ok,
                            "given_image": images.get(norm(g), ""), "expected_image": p.get("image", "")})
    elif t == "group":
        pool = [dict(w, used=False) for w in item["words"]]
        given = answer if isinstance(answer, list) else []
        placed = {}
        for pair in given:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                placed.setdefault(norm(pair[0]), []).append(str(pair[1] or ""))
        for w in pool:
            cats = placed.get(norm(w["text"]), [])
            g = ""
            if w["category"] in cats:
                g = w["category"]
                cats.remove(g)
            elif cats:
                g = cats.pop(0)
            ok = g == w["category"]
            ok_units += ok
            details.append({"word": w["text"], "given": g, "expected": w["category"], "ok": ok})
    elif t == "free":
        text = str(answer or "")[:10000]
        words = len(re.findall(r"[A-Za-zÀ-ÿ']+", text))
        kws = item.get("keywords", [])
        found = [k for k in kws if re.search(r"(?<![\w'])" + re.escape(norm(k)) + r"(?![\w'])", norm(text))]
        frac = (len(found) / len(kws)) if kws else 0.0
        if item.get("min_words") and words < item["min_words"]:
            frac *= 0.5
        if not text.strip():
            frac = 0.0
        ok_units = frac
        needs_review = bool(text.strip())
        details.append({"given": text, "expected": item.get("model_answer", ""), "ok": None,
                        "keywords_found": found, "keywords": kws, "words": words})

    elif t == "speak":
        # practice by imitation: each phrase counts once the student has recorded it.
        # "heard" is what the browser's speech recognition understood (feedback only, when available).
        given = answer if isinstance(answer, list) else []
        for i, p in enumerate(item["phrases"]):
            g = given[i] if i < len(given) and isinstance(given[i], dict) else {}
            heard = str(g.get("heard") or "")[:300]
            ok = bool(g.get("recorded"))
            ok_units += ok
            details.append({"text": p["text"], "recorded": ok, "heard": heard,
                            "match": bool(heard) and norm_loose(heard) == norm_loose(p["text"]), "ok": ok})

    elif t == "video":
        # interactive video: one multiple-choice question at each pause
        given = answer if isinstance(answer, list) else []
        for i, s in enumerate(item["stops"]):
            try:
                g = int(given[i]) if i < len(given) and given[i] is not None else None
            except (TypeError, ValueError):
                g = None
            ok = g == s["correct"]
            ok_units += ok
            details.append({"statement": s["question"], "translation": s.get("translation", ""), "at": s["at"],
                            "given": s["options"][g] if g is not None and 0 <= g < len(s["options"]) else "",
                            "expected": s["options"][s["correct"]], "ok": ok})

    points = item_points(item)
    score = round(points * (ok_units / n_units), 2) if n_units else 0.0
    return {"id": item["id"], "type": t, "score": score, "points": points, "auto_score": score,
            "correct_units": ok_units, "units": n_units, "details": details, "needs_review": needs_review}


def grade_exercise(items, answers):
    answers = answers if isinstance(answers, dict) else {}
    results = [grade_item(it, answers.get(it["id"])) for it in items]
    return {
        "items": results,
        "score": round(sum(r["score"] for r in results), 2),
        "max_score": round(sum(r["points"] for r in results), 2),
        "needs_review": any(r["needs_review"] for r in results),
    }


def to_ten(score, max_score):
    return round(10 * score / max_score, 1) if max_score else 0.0


def final_grade(attempts, policy):
    """attempts: list of dicts with score/max_score, ordered oldest first. Returns 0-10 or None."""
    if not attempts:
        return None
    grades = [to_ten(a["score"], a["max_score"]) for a in attempts]
    if policy == "last":
        return grades[-1]
    if policy == "average":
        return round(sum(grades) / len(grades), 1)
    return max(grades)
