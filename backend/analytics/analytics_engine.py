from backend.database.db import get_connection

def total_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    total = cursor.fetchone()[0]

    conn.close()

    return total

def total_chats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chat_history")

    total = cursor.fetchone()[0]

    conn.close()

    return total

def failed_conversations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM failed_conversations")

    total = cursor.fetchone()[0]

    conn.close()

    return total