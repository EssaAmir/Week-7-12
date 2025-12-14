def create_all_tables(conn):
    cursor = conn.cursor()
    
    # User table for login info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Table for security incidents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """)

    #Table for dataset info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    #Table for IT support tickets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("Database tables created successfully.") #prints the success message