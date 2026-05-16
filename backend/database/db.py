import sqlite3

DATABASE_PATH = (
    "data/chatbot.db"
)

def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    return conn