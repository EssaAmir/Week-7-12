import pandas as pd
from app.data.db import connect_database, BASE_DIR
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file, login_user
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status

def load_csv_data(conn):
    """Loads CSV files into the database using Pandas[cite: 275]."""
    csv_files = {
        'cyber_incidents.csv': 'cyber_incidents',
        'datasets_metadata.csv': 'datasets_metadata',
        'it_tickets.csv': 'it_tickets'
    }
    
    for filename, table_name in csv_files.items():
        file_path = BASE_DIR / "DATA" / filename
        if file_path.exists():
            df = pd.read_csv(file_path)
            # if_exists='append' that adds to existing data
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"Loaded {len(df)} rows from {filename}")
        else:
            print(f"Warning: {filename} not found.")

def main():
    print("---Week 8: Lab DataBase---")
    
    # 1.Connect
    conn= connect_database()
    
    # 2.Setup Schema
    create_all_tables(conn)
    
    # 3.Migrating Users From Week 7
    migrate_users_from_file(conn)
    
    # 4.Load CSV Data (All at once)
    load_csv_data(conn)
    
    print("\n--- TESTING CRUD OPERATIONS ---")
    
    #testing CRUD operations for incidents

    #TEST: Create Incident
    new_id = insert_incident(conn, "2024-12-09", "Phishing", "High", "Open", "Suspicious email", "alice")
    print(f"Created Incident ID: {new_id}")
    
    #TEST: Read Incidents
    df = get_all_incidents(conn)
    print(f"Current Incident Count: {len(df)}")
    print(df.tail(1)) # Show last added
    
    #TEST: Update Incident
    update_incident_status(conn, new_id, "Closed")
    print(f"Updated Incident {new_id} to Closed")

    #TEST: Login
    success, msg = login_user("alice", "secret123") #Change password to match users.txt (later), kept wrong one to test hashing
    print(f"Login Test: {msg}")

    conn.close()

if __name__ == "__main__":
    main()