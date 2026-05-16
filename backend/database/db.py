import sqlite3

from backend.paths import data_path

DATABASE_PATH = str(data_path("chatbot.db"))

def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    return conn