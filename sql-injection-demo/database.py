import sqlite3

def init_db():
    try:
        conn = sqlite3.connect("sqli.db")
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)

        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("alice", "password"))
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("bob", "password"))
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "password"))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

init_db()
