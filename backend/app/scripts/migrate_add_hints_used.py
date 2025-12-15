import sqlite3
import os

# This script adds the 'hints_used' column to the 'game' table by altering its structure.

# Construct the absolute path to the database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'hangman.db')

print(f"Connecting to database at: {db_path}")

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the column already exists to make the script idempotent
    cursor.execute("PRAGMA table_info(game)")
    columns = [info[1] for info in cursor.fetchall()]

    if 'hints_used' not in columns:
        print("Adding 'hints_used' column to 'game' table...")
        # Add the hints_used column to the game table
        cursor.execute("ALTER TABLE game ADD COLUMN hints_used INTEGER DEFAULT 0")

        print("'hints_used' column added successfully.")
    else:
        print("'hints_used' column already exists.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database migration completed successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

