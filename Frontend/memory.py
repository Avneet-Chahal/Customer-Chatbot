import json
import os

FILE_PATH = "chat_history.json"

def load_history():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_message(user, bot):
    history = load_history()
    
    history.append({
        "user": user,
        "bot": bot
    })
    
    with open(FILE_PATH, "w") as f:
        json.dump(history, f, indent=4)