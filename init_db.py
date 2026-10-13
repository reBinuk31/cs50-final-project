
import sqlite3

connection = sqlite3.connect("jobtrack.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        job_title TEXT NOT NULL,
        date_applied TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Applied',
        job_url TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    )
""")

connection.commit()
connection.close()

print("Database initialised successfully!")
