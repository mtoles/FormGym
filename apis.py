from user_features import UserAttributeMeta, UserProfile, BaseUserDbAttr
import sqlite3


class SqlDb:
    def __init__(self, user_profile: UserProfile, file_id: str):
        if file_id == "db_8_0":
            db_content = {}
            # for name, attr_class in UserAttributeMeta.registry.items():
            for name in user_profile.relevant_features:
                attr_class = UserAttributeMeta.registry[name]
                if issubclass(attr_class, BaseUserDbAttr) and attr_class.db == "cr":
                    db_content[name] = getattr(user_profile.features, name)

            # Create an in-memory SQLite DB and insert key-value pairs
            self.conn = sqlite3.connect(":memory:")
            # self.conn = sqlite3.connect("gui_agents_cr.db")
            cursor = self.conn.cursor()
            cursor.execute("CREATE TABLE features (key TEXT PRIMARY KEY, value TEXT)")
            for k, v in db_content.items():
                cursor.execute(
                    "INSERT INTO features (key, value) VALUES (?, ?)", (k, str(v))
                )
        elif file_id == "db_9_0":
            db_content = {}

            # for name, attr_class in UserAttributeMeta.registry.items():
            for name in user_profile.relevant_features:
                attr_class = UserAttributeMeta.registry[name]
                if issubclass(attr_class, BaseUserDbAttr) and attr_class.db == "sec":
                    row_key = attr_class.row
                    if row_key not in db_content:
                        db_content[row_key] = {}
                    db_content[row_key][attr_class.col] = getattr(
                        user_profile.features, name
                    )
                    assert attr_class.col in ["fees", "name"]

            # Create an in-memory SQLite DB with name and fees columns
            self.conn = sqlite3.connect(":memory:")
            cursor = self.conn.cursor()
            cursor.execute(
                "CREATE TABLE features (name TEXT PRIMARY KEY, fees TEXT, service TEXT)"
            )

            # Insert data into the appropriate columns
            for row_key, row_data in db_content.items():
                if "name" in row_data:
                    cursor.execute(
                        "INSERT INTO features (name, fees, service) VALUES (?, NULL, ?)",
                        (str(row_data["name"]), str(row_key)),
                    )
                if "fees" in row_data:
                    # Update the fees column for the corresponding name
                    cursor.execute(
                        "UPDATE features SET fees = ? WHERE name = ?",
                        (str(row_data["fees"]), str(row_data["name"])),
                    )
            # Print the database contents for debugging
            cursor.execute(
                "SELECT Name, Fees, Service FROM features where Service='Underwriters'"
            )
            rows = cursor.fetchall()
            # print("\nDatabase contents:")
            # print("Name | Fees | Service")
            # print("-" * 40)
            # for row in rows:
            #     print(f"{row[0]} | {row[1]} | {row[2]}")
            # print()
            self.conn.commit()
        else:
            raise ValueError(f"Invalid file_id: {file_id}")
        self.conn.commit()
        # self.conn.close()

        # # run a test query, getting all the data
        # cursor.execute("SELECT key, value FROM features")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print("Key:", row[0], "Value:", row[1])
        # print

    def print_db(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM features")
        rows = cursor.fetchall()
        for row in rows:
            print("Key:", row[0], "Value:", row[1])

    def query(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return str(rows)

    def save_to_disk(self, filename: str):
        disk_conn = sqlite3.connect(filename)
        with disk_conn:
            self.conn.backup(disk_conn)
        disk_conn.close()


# Usage:
# sql_db = SqlDb(user_profile)
# sql_db.print_db()
