from backend.database.db import get_connection

def save_feedback(
    username,
    user_message,
    feedback
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO feedback (

        username,
        user_message,
        feedback

    )

    VALUES (?, ?, ?)
    """, (

        username,
        user_message,
        feedback
    ))

    conn.commit()

    conn.close()