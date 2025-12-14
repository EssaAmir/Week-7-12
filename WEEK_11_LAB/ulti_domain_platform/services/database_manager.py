import sqlite3
import os
from typing import Any, Iterable

class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        # Force correct database path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        self._db_path = os.path.join(project_root, 'database', 'platform.db')

        self._connection = None

        # Ensure database folder exists
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)

        # Initialize + migrate schema
        self._initialize_tables()
        self._fix_schema_mismatch()

    def connect(self) -> None:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path, check_same_thread=False)

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def _initialize_tables(self):
        """Creates all required tables if they don't exist."""
        self.connect()
        cur = self._connection.cursor()

        # ---------------- USERS ----------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            );
        """)

        # ---------------- CYBER INCIDENTS ----------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                incident_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                description TEXT,
                date TEXT
            );
        """)

        # ---------------- DATASETS METADATA ----------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                size_bytes INTEGER,
                rows INTEGER,
                source TEXT
            );
        """)

        # ---------------- IT TICKETS ----------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Open',
                assigned_to TEXT
            );
        """)

        self._connection.commit()

    def _fix_schema_mismatch(self):
        """
        Auto-migrates older databases safely
        """
        self.connect()
        cur = self._connection.cursor()

        # ---- CYBER INCIDENTS MIGRATIONS ----
        migrations = [
            ("ALTER TABLE cyber_incidents ADD COLUMN title TEXT",),
            ("ALTER TABLE cyber_incidents ADD COLUMN incident_type TEXT DEFAULT 'General Issue'",),
            ("ALTER TABLE cyber_incidents ADD COLUMN description TEXT DEFAULT ''",),
        ]

        for sql in migrations:
            try:
                cur.execute(sql[0])
                self._connection.commit()
            except sqlite3.OperationalError:
                pass  # Column already exists

    def execute_query(self, sql: str, params: Iterable[Any] = ()):
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur

    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()

    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()
