import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("WS_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "data", "worksheets.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    level TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    name TEXT NOT NULL,
    email TEXT COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    subject TEXT NOT NULL,
    topic TEXT DEFAULT '',
    level TEXT NOT NULL,
    items TEXT NOT NULL DEFAULT '[]',
    max_attempts INTEGER NOT NULL DEFAULT 3,
    grading TEXT NOT NULL DEFAULT 'best',
    show_answers TEXT NOT NULL DEFAULT 'end',
    published INTEGER NOT NULL DEFAULT 0,
    due_date TEXT,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS exercise_classes (
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    PRIMARY KEY (exercise_id, class_id)
);
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    items_snapshot TEXT NOT NULL,
    answers TEXT NOT NULL,
    results TEXT NOT NULL,
    score REAL NOT NULL,
    max_score REAL NOT NULL,
    needs_review INTEGER NOT NULL DEFAULT 0,
    is_preview INTEGER NOT NULL DEFAULT 0,
    feedback TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_attempts_ex_st ON attempts(exercise_id, student_id);
CREATE TABLE IF NOT EXISTS attempt_grants (
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    extra INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (exercise_id, student_id)
);
"""


def _connect():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


@contextmanager
def conn():
    c = _connect()
    try:
        yield c
        c.commit()
    finally:
        c.close()


MIGRATIONS = """
CREATE TABLE IF NOT EXISTS class_teachers (
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (class_id, teacher_id)
);
CREATE TABLE IF NOT EXISTS password_resets (
    id INTEGER PRIMARY KEY,
    token_hash TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TEXT NOT NULL,
    used_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def _migrate_users(c):
    """v2: roles admin/teacher/student (no CHECK constraint) + email column."""
    cols = [r["name"] for r in c.execute("PRAGMA table_info(users)").fetchall()]
    if "email" in cols:
        return
    c.execute("PRAGMA foreign_keys = OFF")
    c.executescript("""
    BEGIN;
    CREATE TABLE users_v2 (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL COLLATE NOCASE,
        name TEXT NOT NULL,
        email TEXT COLLATE NOCASE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    INSERT INTO users_v2 (id, username, name, password_hash, role, class_id, active, created_at)
        SELECT id, username, name, password_hash, role, class_id, active, created_at FROM users;
    DROP TABLE users;
    ALTER TABLE users_v2 RENAME TO users;
    COMMIT;
    """)
    c.execute("PRAGMA foreign_keys = ON")


def init():
    c = _connect()
    try:
        c.execute("PRAGMA journal_mode = WAL")
        c.executescript(SCHEMA)
        _migrate_users(c)
        c.executescript(MIGRATIONS)
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email) WHERE email IS NOT NULL AND email <> ''")
        c.commit()
    finally:
        c.close()


def all(sql, params=()):
    with conn() as c:
        return [dict(r) for r in c.execute(sql, params).fetchall()]


def one(sql, params=()):
    with conn() as c:
        r = c.execute(sql, params).fetchone()
        return dict(r) if r else None


def run(sql, params=()):
    with conn() as c:
        cur = c.execute(sql, params)
        return cur.lastrowid
