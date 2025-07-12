import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL
);
""")

cursor.executemany("""
INSERT INTO users (name, email, age) VALUES (?, ?, ?)
""", [
    ("Faith Okoth", "faith.okoth@example.com", 28),
    ("Idah Khumalo", "idah.khumalo@example.com", 31),
    ("Junior Boy", "junior.boy@example.com", 21),
    ("Crawford Cartwright", "crawford@example.com", 44),
    ("Lerato Mokoena", "lerato.m@example.com", 39),
    ("Mandisa Mthembu", "mandisa.m@example.com", 51),
])

conn.commit()
conn.close()

