import pandas as pd

from app.db.database import engine, sqlite_engine


def transfer_table(table_name):
    # Create SQLite session
    sqlite_conn = sqlite_engine.connect()

    # Read data from SQLite
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, sqlite_conn)

    # Close SQLite connection
    sqlite_conn.close()

    # Create PostgreSQL session
    postgres_conn = engine.connect()

    # Write data to PostgreSQL
    df.to_sql(table_name, postgres_conn, if_exists='replace', index=False)

    # Close PostgreSQL connection
    postgres_conn.close()