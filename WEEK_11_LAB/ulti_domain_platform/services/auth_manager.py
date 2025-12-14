from typing import Optional
import bcrypt  # Using bcrypt as per Week 7 guidelines
from models.user import User
from services.database_manager import DatabaseManager

class AuthManager:
    """Handles user registration and login."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str, role: str = "user"):
        #Hash password with salt before storage
        #encode() converts string to bytes, which bcrypt requires
        salt= bcrypt.gensalt()
        password_hash= bcrypt.hashpw(password.encode('utf-8'), salt)
        
        #Store the hash (as a string) in the database
        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash.decode('utf-8'), role),
        )

    def login_user(self, username: str, password: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row

        # - Verify password against stored hash
        #we must encode the input password to bytes and encode the stored hash to bytes
        if bcrypt.checkpw(password.encode('utf-8'), password_hash_db.encode('utf-8')):
            return User(username_db, password_hash_db, role_db)

        return None