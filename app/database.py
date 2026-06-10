# database.py

import sqlite3
from pathlib import Path

def get_db_connection(db_path: Path = Path("data/tracker.db")) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)

def initialize_database(db_path: Path = Path("data/tracker.db")) -> None:
    with get_db_connection(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            goal TEXT NOT NULL,
            calorie_target INTEGER NOT NULL,
            protein_target REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS daily_log(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            log_date TEXT NOT NULL,
            weight_lbs REAL NOT NULL,
            calories INTEGER NOT NULL,
            protein_g INTEGER NOT NULL,
            steps INTEGER NULL,
            notes TEXT NULL
        );

        CREATE TABLE IF NOT EXISTS tdee_estimates(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            estimate_date TEXT NOT NULL,
            estimated_tdee REAL NOT NULL,
            confidence REAL NOT NULL,
            weeks_of_data INTEGER NOT NULL
        );
    """)
        
def save_log_entry(
        user_id: int,
        log_date: str,
        weight_lbs: float,
        calories: int,
        protein_g: int,
        steps: int = None,
        notes: str = None,
        db_path: Path = Path("data/tracker.db")
) -> None:
    with get_db_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO daily_log (user_id, log_date, weight_lbs, calories, protein_g, steps, notes) VALUES (?,?,?,?,?,?,?)",
            (user_id, log_date, weight_lbs, calories, protein_g, steps, notes)
        )

def get_weights_for_user(
        user_id: int,
        limit: int = 30,
        db_path: Path = Path("data/tracker.db")
) -> list[tuple]:
    with get_db_connection(db_path) as conn:
        result = conn.execute(
            """SELECT weight_lbs, log_date FROM daily_log 
            WHERE user_id = ?
            ORDER BY log_date DESC
            LIMIT ?""",
            (user_id, limit)
        )
        return result.fetchall()
