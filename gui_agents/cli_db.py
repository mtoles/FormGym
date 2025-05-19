#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path

import pandas as pd

def get_db_connection(db_file=None):
    db_path = Path(__file__).parent / db_file
    if not db_path.exists():
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)
    return sqlite3.connect(db_path)
        
def execute_query_df(conn, query):
    try:
        # Check if query is a SELECT query
        if not query.strip().upper().startswith("SELECT"):
            print(
                "Error: Only SELECT queries are allowed. This is a read-only database."
            )
            return

        cursor = conn.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        if results:
            # Get column names
            columns = [description[0] for description in cursor.description]

        return pd.DataFrame(results, columns=columns,)
    
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
    
def execute_query(conn, query):
    result = execute_query_df(conn, query).to_string(index=False)
    
    if result:
        print(result)


def main(db_file=None):
    print("SQLite Database Query Tool")
    print("Type your SQL queries (type 'exit' or 'quit' to exit)")
    print("Type 'tables' to list all tables")
    print("-" * 50)

    conn = get_db_connection(db_file=db_file)

    try:
        while True:
            try:
                query = input("\nEnter SQL query> ").strip()

                if query.lower() in ("exit", "quit"):
                    break
                elif query.lower() == "tables":
                    execute_query(
                        conn, "SELECT name FROM sqlite_master WHERE type='table';"
                    )
                elif query:
                    execute_query(conn, query)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
