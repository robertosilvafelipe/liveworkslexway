"""Create demo data: teacher Lisa, student Felipe, an A1 class and example exercises.

Usage: python -m app.seed --teacher-password X --student-password Y
Safe to run again: existing users/class/exercises (matched by username/title) are kept.
"""
import argparse
import json

from . import db, grading
from .auth import hash_password

VERB_TO_BE = {
    "title": "Verb To Be — Affirmative, Negative & Questions",
    "description": "Practice the verb to be (am / is / are). Read each instruction carefully. Good luck! 🍀",
    "subject": "Grammar",
    "topic": "Verb to be",
    "level": "A1",
    "items": [
        {"type": "dropdown", "prompt": "Choose am, is or are.",
         "text": "1. I [*am|is|are] from Brazil.\n2. She [am|*is|are] my teacher.\n3. We [am|is|*are] students.\n"
                 "4. It [am|*is|are] a big city.\n5. You [am|is|*are] very nice.\n6. My parents [am|is|*are] at home."},
        {"type": "fill", "prompt": "Complete with the NEGATIVE form of the verb to be.",
         "text": "1. He [isn't|is not] at school today.\n2. They [aren't|are not] from Italy.\n"
                 "3. I [am not|'m not] hungry.\n4. The cat [isn't|is not] black.\n5. We [aren't|are not] late."},
        {"type": "choice", "prompt": "Which question is correct?",
         "options": ["She is a doctor?", "Is she a doctor?", "Are she a doctor?", "Is a doctor she?"], "correct": 1},
        {"type": "truefalse",
         "prompt": "Read the text and choose True or False.\n\n"
                   "\"Hi! My name is Anna. I am 25 years old and I am from Canada. My brother Tom is a student. "
                   "He is 19. Our parents are teachers.\"",
         "statements": [
             {"text": "Anna is from Canada.", "answer": True},
             {"text": "Tom is a teacher.", "answer": False},
             {"text": "Tom is 19 years old.", "answer": True},
             {"text": "Anna's parents are doctors.", "answer": False},
         ]},
        {"type": "order", "prompt": "Put the words in the correct order to make a question.",
         "tokens": ["Are", "you", "from", "Brazil?"], "alternatives": []},
        {"type": "order", "prompt": "Put the words in the correct order.",
         "tokens": ["We", "are", "not", "at", "school", "today."], "alternatives": ["Today we are not at school."]},
        {"type": "match", "prompt": "Match the questions to the answers.",
         "pairs": [
             {"left": "Are you a student?", "right": "Yes, I am."},
             {"left": "Is he your brother?", "right": "No, he isn't. He's my cousin."},
             {"left": "Where are they from?", "right": "They're from Japan."},
             {"left": "How old is she?", "right": "She's twelve."},
             {"left": "What's your name?", "right": "My name is Felipe."},
         ]},
        {"type": "group", "prompt": "Which form of the verb to be goes with each subject?",
         "categories": ["am", "is", "are"],
         "words": [
             {"text": "I", "category": "am"}, {"text": "he", "category": "is"}, {"text": "she", "category": "is"},
             {"text": "it", "category": "is"}, {"text": "you", "category": "are"}, {"text": "we", "category": "are"},
             {"text": "they", "category": "are"}, {"text": "my mother", "category": "is"},
             {"text": "Tom and Anna", "category": "are"},
         ]},
        {"type": "free", "prompt": "Write 4–5 sentences about you. Use the verb to be.\n(name, age, country, job, favorite color)",
         "model_answer": "My name is Felipe. I am 30 years old. I am from Brazil. I am a student. My favorite color is blue.",
         "keywords": ["my name is", "I am", "from"], "min_words": 15, "points": 5},
    ],
}

VOCAB_COUNTRIES = {
    "title": "Countries & Nationalities",
    "description": "Vocabulary practice: countries and nationalities with the verb to be.",
    "subject": "Vocabulary",
    "topic": "Countries & nationalities",
    "level": "A1",
    "items": [
        {"type": "match", "prompt": "Match the country to the nationality.",
         "pairs": [
             {"left": "🇧🇷 Brazil", "right": "Brazilian"}, {"left": "🇯🇵 Japan", "right": "Japanese"},
             {"left": "🇪🇸 Spain", "right": "Spanish"}, {"left": "🇺🇸 The USA", "right": "American"},
             {"left": "🇫🇷 France", "right": "French"},
         ]},
        {"type": "fill", "prompt": "Complete the sentences with the nationality.",
         "text": "1. Pedro is from Mexico. He is [Mexican].\n2. Yuki and Ken are from Japan. They are [Japanese].\n"
                 "3. Emma is from England. She is [English|British].\n4. I am from Italy. I am [Italian]."},
        {"type": "group", "prompt": "Group the nationalities by ending.",
         "categories": ["-ian / -an", "-ese", "-ish"],
         "words": [
             {"text": "Brazilian", "category": "-ian / -an"}, {"text": "Italian", "category": "-ian / -an"},
             {"text": "American", "category": "-ian / -an"}, {"text": "Chinese", "category": "-ese"},
             {"text": "Portuguese", "category": "-ese"}, {"text": "English", "category": "-ish"},
             {"text": "Spanish", "category": "-ish"}, {"text": "Turkish", "category": "-ish"},
         ]},
    ],
}


def upsert_user(username, name, role, password, class_id=None):
    u = db.one("SELECT id FROM users WHERE username=?", (username,))
    if u:
        print(f"user {username} already exists (id {u['id']}) — password unchanged")
        return u["id"]
    uid = db.run("INSERT INTO users (username, name, password_hash, role, class_id) VALUES (?,?,?,?,?)",
                 (username, name, hash_password(password), role, class_id))
    print(f"created {role} {username}")
    return uid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teacher-password", required=True)
    ap.add_argument("--student-password", required=True)
    args = ap.parse_args()
    db.init()

    cls = db.one("SELECT id FROM classes WHERE name=?", ("A1 — Turma da Lisa",))
    class_id = cls["id"] if cls else db.run("INSERT INTO classes (name, level, description) VALUES (?,?,?)",
                                            ("A1 — Turma da Lisa", "A1", "Turma de exemplo (iniciantes)"))
    teacher_id = upsert_user("lisa", "Lisa", "teacher", args.teacher_password)
    upsert_user("felipe", "Felipe", "student", args.student_password, class_id)
    db.run("INSERT OR IGNORE INTO class_teachers (class_id, teacher_id) VALUES (?,?)", (class_id, teacher_id))

    for spec in (VERB_TO_BE, VOCAB_COUNTRIES):
        if db.one("SELECT id FROM exercises WHERE title=?", (spec["title"],)):
            print(f"exercise '{spec['title']}' already exists")
            continue
        items = grading.validate_items(spec["items"])
        eid = db.run("""INSERT INTO exercises (title, description, subject, topic, level, items, max_attempts, grading,
                        show_answers, published, created_by) VALUES (?,?,?,?,?,?,3,'best','end',1,?)""",
                     (spec["title"], spec["description"], spec["subject"], spec["topic"], spec["level"],
                      json.dumps(items, ensure_ascii=False), teacher_id))
        db.run("INSERT INTO exercise_classes VALUES (?,?)", (eid, class_id))
        print(f"created exercise '{spec['title']}' ({len(items)} items)")


if __name__ == "__main__":
    main()
