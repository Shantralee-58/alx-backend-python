import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    );
''')

# Insert sample users
cursor.executemany('''
    INSERT INTO users (name, email) VALUES (?, ?)
''', [
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Carol Jones', 'carol@example.com'),
])

conn.commit()
conn.close()
print("Database initialized with sample data.")

