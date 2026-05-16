import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from backend.database.db import get_connection


def create_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()


def verify_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row or not check_password_hash(row[0], password):
        return False, "Invalid username or password."
    return True, username
