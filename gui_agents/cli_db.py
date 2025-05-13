#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path


def get_db_connection():
    db_path = Path(__file__).parent / "gui_agents.db"
    if not db_path.exists():
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)
    return sqlite3.connect(db_path)


def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # If it's a SELECT query, fetch and display results
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            if results:
                # Get column names
                columns = [description[0] for description in cursor.description]
                # Print column names
                print("\n" + " | ".join(columns))
                print("-" * (sum(len(col) for col in columns) + 3 * len(columns)))
                # Print results
                for row in results:
                    print(" | ".join(str(value) for value in row))
                print(f"\n{len(results)} rows returned")
            else:
                print("No results found")
        else:
            # For non-SELECT queries, commit the changes
            conn.commit()
            print("Query executed successfully")

    except sqlite3.Error as e:
        print(f"Error executing query: {e}")


def main():
    print("SQLite Database Query Tool")
    print("Type your SQL queries (type 'exit' or 'quit' to exit)")
    print("Type 'tables' to list all tables")
    print("-" * 50)

    conn = get_db_connection()

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
