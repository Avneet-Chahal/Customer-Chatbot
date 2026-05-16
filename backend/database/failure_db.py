from backend.database.db import (
    get_connection
)

def save_failure(

    username,

    user_message,

    bot_response,

    reason
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO failed_conversations (

        username,

        user_message,

        bot_response,

        reason

    )

    VALUES (?, ?, ?, ?)
    """, (

        username,

        user_message,

        bot_response,

        reason
    ))

    conn.commit()

    conn.close()