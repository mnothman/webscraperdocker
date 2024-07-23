import sqlite3

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (title TEXT, description TEXT, page INTEGER)''')
    conn.commit()
    conn.close()

def save_to_database(db_path, data):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany('INSERT INTO items (title, description, page) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()
