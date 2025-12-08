import bcrypt
import sqlite3
from pathlib import Path

# Helper to locate the DB correctly
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "DATA" / "intelligence_platform.db"

def connect_database():
    return sqlite3.connect(str(DB_PATH))

def migrate_users_from_file(conn, filename="users.txt"):
    """Reads users.txt and inserts them into the DB."""
    file_path = BASE_DIR / "DATA" / filename
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    cursor = conn.cursor()
    count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                username = parts[0]
                raw_password = parts[1] 
                role = parts[2] if len(parts) > 2 else 'user'
                
                # Hash the password
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(raw_password.encode(), salt).decode()

                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                        (username, password_hash, role)
                    )
                    count += 1
                except Exception as e:
                    print(f"Error adding {username}: {e}")

    conn.commit()
    print(f"✓ Migrated {count} users from file.")

def login_user(username, password):
    """Authenticate a user."""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Fetch the password hash for the user
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        # Verify the provided password against the stored hash
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return True, "Login successful"
    return False, "Invalid credentials"