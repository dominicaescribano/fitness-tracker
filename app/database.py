# database.py

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    return psycopg2.connect(database_url)

def initialize_database() -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    calorie_target INTEGER NOT NULL,
                    protein_target FLOAT NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_log(
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    log_date TEXT NOT NULL,
                    weight_lbs FLOAT NOT NULL,
                    calories INTEGER NOT NULL,
                    protein_g INTEGER NOT NULL,
                    steps INTEGER NULL,
                    notes TEXT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tdee_estimates(
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    estimate_date TEXT NOT NULL,
                    estimated_tdee FLOAT NOT NULL,
                    confidence FLOAT NOT NULL,
                    weeks_of_data INTEGER NOT NULL
                );
            """)
        conn.commit()
        
def save_log_entry(
        user_id: int,
        log_date: str,
        weight_lbs: float,
        calories: int,
        protein_g: int,
        steps: int = None,
        notes: str = None
) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO daily_log (user_id, log_date, weight_lbs, calories, protein_g, steps, notes) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (user_id, log_date, weight_lbs, calories, protein_g, steps, notes)
            )
        conn.commit()

def get_weights_for_user(
        user_id: int,
        limit: int = 30
) -> list[tuple]:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT log_date, weight_lbs FROM daily_log 
                WHERE user_id = %s
                ORDER BY log_date DESC
                LIMIT %s""",
                (user_id, limit)
            )
            return cursor.fetchall()

def get_logs_for_user(
        user_id: int,
        limit: int = 30
) -> list[tuple]:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT log_date, weight_lbs, calories, protein_g, steps, notes FROM daily_log 
                WHERE user_id = %s
                ORDER BY log_date DESC
                LIMIT %s""",
                (user_id, limit)
            )
            return cursor.fetchall()

def get_or_create_user(
        name: str,
        goal: str = "maintain",
        calorie_target: int = 2000,
        protein_target: float = 150.0
) -> int:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE name = %s",
                (name,)
            )
            existing = cursor.fetchone()
            if existing:
                return existing[0]
            else:
                cursor.execute("INSERT INTO users (name, goal, calorie_target, protein_target) VALUES (%s,%s,%s,%s) RETURNING id",
                                    (name, goal, calorie_target, protein_target)
                                    )
                conn.commit()
                return cursor.fetchone()[0]
