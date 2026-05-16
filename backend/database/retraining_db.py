from backend.database.db import get_connection

def save_retraining_data(
    user_message,
    correct_intent
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO retraining_data (

        user_message,
        correct_intent

    )

    VALUES (?, ?)
    """, (

        user_message,
        correct_intent
    ))

    conn.commit()

    conn.close()