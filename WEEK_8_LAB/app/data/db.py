import sqlite3
from pathlib import Path

# This finds the correct path to your DATA folder no matter where you run the code from
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "DATA" / "intelligence_platform.db"

def connect_database():
    # connects to the database file
    return sqlite3.connect(str(DB_PATH))