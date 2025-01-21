import sqlite3

# Define the database file path
db_path = 'database.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check if the STUDENTS table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STUDENTS';")
table_exists = cur.fetchone()

if table_exists:
    print("The STUDENTS table exists.")
else:
    # Create the STUDENTS table if it does not exist
    cur.execute('''
        CREATE TABLE STUDENTS (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            father TEXT,
            num INTEGER,
            email TEXT,
            rank INTEGER,
            telephone INTEGER,
            file TEXT
        )
    ''')
    print("The STUDENTS table has been created successfully.")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()