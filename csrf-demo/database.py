import sqlite3

def init_db():
    conn = sqlite3.connect("csrf.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL
    )""")

    # Add two users if not exists
    users = [("alice", "password", 100), ("bob", "password", 50)]
    for u in users:
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", u)

    conn.commit()
    conn.close()
