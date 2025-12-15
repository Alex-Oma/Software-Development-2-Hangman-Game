import sqlite3
import os

# This script adds the 'initial_attempts' column to the 'game' table by altering the table schema.

# Construct the absolute path to the database file
# The script is in backend/app/scripts, and the DB is in backend/app/database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'hangman.db')

print(f"Connecting to database at: {db_path}")

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the column already exists to make the script idempotent
    cursor.execute("PRAGMA table_info(game)")
    columns = [info[1] for info in cursor.fetchall()]

    if 'initial_attempts' not in columns:
        print("Adding 'initial_attempts' column to 'game' table...")
        # Add the initial_attempts column to the game table
        cursor.execute("ALTER TABLE game ADD COLUMN initial_attempts INTEGER")

        # Set a default value for existing rows.
        print("Updating existing rows with a default value for 'initial_attempts'...")
        cursor.execute("UPDATE game SET initial_attempts = 6 WHERE initial_attempts IS NULL")

        print("'initial_attempts' column added and updated successfully.")
    else:
        print("'initial_attempts' column already exists.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database migration completed successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

