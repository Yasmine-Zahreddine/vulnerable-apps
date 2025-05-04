import sqlite3

def init_db():
    try:
        conn = sqlite3.connect("idor.db")
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)

        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("alice", "password"))
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("bob", "password"))

        c.execute("INSERT OR IGNORE INTO messages (id, user_id, content) VALUES (?, ?, ?)", (1, 1, "Hello, this is a secret message for Alice"))
        c.execute("INSERT OR IGNORE INTO messages (id, user_id, content) VALUES (?, ?, ?)", (2, 2, "Hi, this is a secret message for Bob"))
        c.execute("INSERT OR IGNORE INTO messages (id, user_id, content) VALUES (?, ?, ?)", (3, 2, "Hi, this is another secret message for Bob"))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

init_db()
