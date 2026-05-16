from backend.database.db import get_connection

def save_memory(
    username,
    memory_key,
    memory_value,
    priority=1
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO memory (

        username,
        memory_key,
        memory_value,
        priority

    )

    VALUES (?, ?, ?, ?)
    """, (

        username,
        memory_key,
        memory_value,
        priority
    ))

    conn.commit()

    conn.close()

def get_memory(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT memory_key, memory_value

    FROM memory

    WHERE username = ?
    """, (username,))

    memories = cursor.fetchall()

    conn.close()

    return memories