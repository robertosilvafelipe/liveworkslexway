"""Shared helper for the seed_* scripts that fill public course pages (/curso/<slug>)."""
import hashlib
import json
import os
import random
import re

from . import db, grading


STATIC = os.path.join(os.path.dirname(__file__), "static")


def _versioned(url):
    """/static/... -> /static/...?v=<content hash>, so browsers fetch a file again when it changes (e.g. new voices)."""
    if not isinstance(url, str) or not url.startswith("/static/"):
        return url
    path = os.path.join(STATIC, url.split("?")[0][len("/static/"):])
    if not os.path.exists(path):
        return url
    with open(path, "rb") as f:
        return url.split("?")[0] + "?v=" + hashlib.md5(f.read()).hexdigest()[:8]


def _with_versions(items):
    for it in items:
        for k in ("audio", "video", "subtitles", "poster"):
            if it.get(k):
                it[k] = _versioned(it[k])
        if it.get("phrases"):
            it["phrases"] = [dict(p, audio=_versioned(p.get("audio"))) for p in it["phrases"]]
        if it.get("pairs"):
            it["pairs"] = [dict(p, image=_versioned(p["image"])) if p.get("image") else p for p in it["pairs"]]
    return items


def _mix(spec):
    """Shuffle choice and dropdown options so the right answer isn't always first (specs list it first).

    Seeded by the title, so re-running a seed keeps the same order.
    """
    rng = random.Random(spec["title"])
    items = []
    for it in spec["items"]:
        it = dict(it)
        if it["type"] == "choice":
            order = list(range(len(it["options"])))
            rng.shuffle(order)
            it["options"] = [it["options"][i] for i in order]
            it["correct"] = order.index(it["correct"])
        elif it["type"] == "video":
            stops = []
            for s in it["stops"]:
                order = list(range(len(s["options"])))
                rng.shuffle(order)
                stops.append(dict(s, options=[s["options"][i] for i in order], correct=order.index(s["correct"])))
            it["stops"] = stops
        elif it["type"] == "dropdown":
            def shuffle_blank(m):
                opts = m.group(1).split("|")
                rng.shuffle(opts)
                return "[" + "|".join(opts) + "]"
            it["text"] = re.sub(r"\[([^\[\]]*\|[^\[\]]*)\]", shuffle_blank, it["text"])
        items.append(it)
    return items


def publish(slug, level, specs):
    """Create or update each spec (title, description, topic, items, optional subject/lesson) on the page.

    Exercises are matched by title within the page; an update keeps the id, so links and past attempts stay valid.
    """
    db.init()
    admin = db.one("SELECT id FROM users WHERE role='admin' ORDER BY id")
    for spec in specs:
        items = json.dumps(grading.validate_items(_with_versions(_mix(spec))), ensure_ascii=False)
        values = (spec["description"], spec.get("subject", "Grammar"), spec["topic"], level, items, spec.get("lesson"))
        old = db.one("SELECT id FROM exercises WHERE title=? AND public_slug=?", (spec["title"], slug))
        if old:
            db.run("""UPDATE exercises SET description=?, subject=?, topic=?, level=?, items=?, public_lesson=?,
                      updated_at=CURRENT_TIMESTAMP WHERE id=?""", values + (old["id"],))
            print(f"updated exercise '{spec['title']}' ({len(spec['items'])} items)")
        else:
            db.run("""INSERT INTO exercises (description, subject, topic, level, items, public_lesson, title, public_slug,
                      max_attempts, grading, show_answers, published, created_by) VALUES (?,?,?,?,?,?,?,?,0,'best','always',1,?)""",
                   values + (spec["title"], slug, admin["id"] if admin else None))
            print(f"created exercise '{spec['title']}' ({len(spec['items'])} items)")
    print(f"page: /curso/{slug}")
