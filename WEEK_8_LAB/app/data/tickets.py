import pandas as pd

def get_all_tickets(conn):
    return pd.read_sql_query("SELECT * FROM it_tickets", conn)