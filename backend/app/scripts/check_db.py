# This script checks if the hangman database exists and lists its tables.
import sqlite3, pathlib
p = pathlib.Path('backend/app/database/hangman.db')
print('exists', p.exists(), p)
if p.exists():
    conn = sqlite3.connect(str(p))
    try:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print('tables:', tables)
    finally:
        conn.close()

