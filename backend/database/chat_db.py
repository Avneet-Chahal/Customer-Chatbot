from backend.database.db import (
    get_connection
)

def save_chat(

    username,

    user_message,

    bot_response,

    intent,

    emotion,

    confidence
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_history (

        username,

        user_message,

        bot_response,

        intent,

        emotion,

        confidence

    )

    VALUES (?, ?, ?, ?, ?, ?)
    """, (

        username,

        user_message,

        bot_response,

        intent,

        emotion,

        confidence
    ))

    conn.commit()

    conn.close()