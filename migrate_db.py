import sqlite3

conn = sqlite3.connect("fitbuddy.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]

if "feedback" not in columns:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN feedback TEXT"
    )
    print("Feedback column added successfully!")
else:
    print("Feedback column already exists!")

conn.commit()
conn.close()

print("Database migration completed!")