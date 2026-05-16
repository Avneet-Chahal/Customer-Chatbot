"""Run during Render build to prepare NLTK data and the SQLite database."""

import ssl
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import nltk

from backend.database.init_db import initialize_database


def main() -> None:
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except Exception:
        pass

    for resource in ("stopwords", "punkt"):
        try:
            nltk.download(resource, quiet=True)
            print(f"NLTK: downloaded {resource}")
        except Exception as exc:
            print(f"NLTK: skipped {resource} ({exc})")

    initialize_database()
    print("Database initialized.")


if __name__ == "__main__":
    main()
