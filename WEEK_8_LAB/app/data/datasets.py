import pandas as pd

def get_all_datasets(conn):
    return pd.read_sql_query("SELECT * FROM datasets_metadata", conn)