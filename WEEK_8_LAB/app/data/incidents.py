import pandas as pd
from app.data.db import connect_database

#creating incident
def insert_incident(conn, date, incident_type, severity, status, description, reported_by):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

#function for reading incidents
def get_all_incidents(conn):
    # Using Pandas to read SQL - efficient and returns a DataFrame
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

#function for updating incident
def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()

#function for deleting incident
def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()