import sqlite3
import pandas as pd
import bcrypt
import os
from pathlib import Path

# setting up the paths for data
DATA_DIR =Path("DATA")
DB_PATH =DATA_DIR / "intelligence_platform.db"

# simple function to connect to the db
def connect_database():
    # this will create the file if it doesn't exist yet
    return sqlite3.connect(str(DB_PATH))

# creates all the tables we need for the lab
def create_all_tables(conn):
    cursor =conn.cursor()
    
    # table for users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # table for cyber incidents
    # linking reported_by to the users table
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

    # table for datasets metadata
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

    # table for IT tickets
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
    
    # save everything
    conn.commit()
    print("Tables created.")

# function to move old users from the txt file to the new db
def migrate_users(conn):
    user_file = DATA_DIR / "users.txt"
    
    # check if file exists first
    if not user_file.exists():
        print("users.txt missing, skipping this part.")
        return

    cursor= conn.cursor()
    count= 0
    
    with open(user_file, 'r') as f:
        for line in f:
            # clean up the line and split by comma
            parts= line.strip().split(',')
            
            # make sure we have enough data (user, hash, role)
            if len(parts) >= 2:
                username, password_hash =parts[0], parts[1]
                try:
                    # try inserting, ignore if username is taken
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    count += 1
                except sqlite3.Error:
                    continue # skip if there's a db error
                    
    conn.commit()
    print(f"Moved {count} users to database.")

# loads all the csv files using pandas
def load_csv_data(conn):
    # list of files and their matching table names
    files_to_load = [
        ("cyber_incidents.csv", "cyber_incidents"),
        ("datasets_metadata.csv", "datasets_metadata"),
        ("it_tickets.csv", "it_tickets")
    ]
    
    total_rows= 0
    
    for filename, table_name in files_to_load:
        file_path = DATA_DIR / filename
        
        if file_path.exists():
            try:
                # pandas makes this super easy
                df = pd.read_csv(file_path)
                # 'append' adds to existing data, index=False skips the row numbers
                df.to_sql(table_name, conn, if_exists='append', index=False)
                
                print(f"Loaded {len(df)} rows into {table_name}")
                total_rows += len(df)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"Couldn't find {filename}")
            
    return total_rows

# --- CRUD FUNCTIONS ---

# adds a new incident to the db
def insert_incident(conn, date, incident_type, severity, status, description, reported_by):
    cursor = conn.cursor()
    # using ? placeholders here to be safe from SQL injection
    sql= """
    INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid # returns the id of the new row

# gets everything from the incidents table
def get_all_incidents(conn):
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

# updates the status of a specific incident
def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()

# deletes an incident by id
def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()

# main function to run everything
def main():
    print("--- Setting up Week 8 Lab ---")
    
    # 1. connect to db
    conn = connect_database()
    
    # 2. setup tables and data
    create_all_tables(conn)
    migrate_users(conn)
    load_csv_data(conn)
    
    print("\n--- Testing the CRUD functions ---")
    
    # trying to create a new one
    new_id = insert_incident(conn, "2024-12-01", "Hacking", "Critical", "Open", "Server breach", "admin")
    print(f"Test: Made new incident with ID {new_id}")
    
    # reading them back
    df = get_all_incidents(conn)
    print(f"Test: Read {len(df)} total incidents")
    
    # updating one
    update_incident_status(conn, new_id, "Resolved")
    print(f"Test: Updated incident {new_id} to Resolved")
    
    # deleting it
    delete_incident(conn, new_id)
    print(f"Test: Deleted incident {new_id}")
    
    conn.close()
    print("\nDone with Week 8!")

if __name__ == "__main__":
    main()