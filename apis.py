from user_features import UserAttributeMeta, UserProfile, BaseUserDbAttr
import sqlite3


class SqlDb:
    def __init__(self, user_profile: UserProfile):
        db_content = {}
        for name, attr_class in UserAttributeMeta.registry.items():
            if issubclass(attr_class, BaseUserDbAttr):
                db_content[name] = getattr(user_profile.features, name)

        # Create an in-memory SQLite DB and insert key-value pairs
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE features (key TEXT PRIMARY KEY, value TEXT)")
        for k, v in db_content.items():
            cursor.execute("INSERT INTO features (key, value) VALUES (?, ?)", (k, str(v)))
        self.conn.commit()

        # run a test query, getting all the data
        # cursor.execute("SELECT key, value FROM features")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print("Key:", row[0], "Value:", row[1])
        print

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
        

# Usage:
# sql_db = SqlDb(user_profile)
# sql_db.print_db()

