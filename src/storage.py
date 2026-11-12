import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


def get_connection(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(habit_id, log_date),
            FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def add_habit(conn, name):
    name = name.strip()
    if not name:
        raise ValueError("El nombre del hábito no puede estar vacío")
    now = datetime.utcnow().isoformat(timespec="seconds")
    try:
        conn.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, now))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"El hábito '{name}' ya existe")


def list_habits(conn):
    cur = conn.execute("SELECT id, name, created_at FROM habits ORDER BY name COLLATE NOCASE")
    return [dict(r) for r in cur.fetchall()]


def _get_habit(conn, name):
    cur = conn.execute("SELECT id, name FROM habits WHERE name = ? COLLATE NOCASE", (name.strip(),))
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Hábito no encontrado: {name}")
    return row


def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Fecha inválida, usa formato YYYY-MM-DD")


def log_habit(conn, name, date_str=None):
    habit = _get_habit(conn, name)
    log_date = _parse_date(date_str) if date_str else datetime.now().date()
    now = datetime.utcnow().isoformat(timespec="seconds")
    try:
        conn.execute(
            "INSERT INTO logs (habit_id, log_date, created_at) VALUES (?, ?, ?)",
            (habit["id"], log_date.isoformat(), now),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"El hábito '{habit['name']}' ya fue registrado en {log_date.isoformat()}")
    return log_date.isoformat()


def get_history(conn, name):
    habit = _get_habit(conn, name)
    cur = conn.execute(
        "SELECT log_date FROM logs WHERE habit_id = ? ORDER BY log_date DESC",
        (habit["id"],),
    )
    return [r["log_date"] for r in cur.fetchall()]


def get_streak(conn, name, today=None):
    habit = _get_habit(conn, name)
    today = today or datetime.now().date()
    cur = conn.execute("SELECT log_date FROM logs WHERE habit_id = ?", (habit["id"],))
    dates = {datetime.strptime(r["log_date"], "%Y-%m-%d").date() for r in cur.fetchall()}
    if not dates:
        return 0
    # current streak: consecutive days ending today or yesterday
    if today in dates:
        current = today
    elif (today - timedelta(days=1)) in dates:
        current = today - timedelta(days=1)
    else:
        return 0
    streak = 0
    while current in dates:
        streak += 1
        current -= timedelta(days=1)
    return streak
