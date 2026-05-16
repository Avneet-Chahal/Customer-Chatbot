from backend.database.db import (
    get_connection
)

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================
    # USERS TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT
    )
    """)

    # =========================
    # CHAT HISTORY
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        user_message TEXT,

        bot_response TEXT,

        intent TEXT,

        emotion TEXT,

        confidence TEXT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # FAILED CONVERSATIONS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS failed_conversations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        user_message TEXT,

        bot_response TEXT,

        reason TEXT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()

    print(
        "Database initialized successfully"
    )

if __name__ == "__main__":

    initialize_database()