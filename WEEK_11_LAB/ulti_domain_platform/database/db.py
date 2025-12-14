import sqlite3
from pathlib import Path

# Use a DB file path relative to this package so the path resolves consistently
BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = str(BASE_DIR / "platform.db")

def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create the Users table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # Create the Cyber Incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on import
initialize_database()