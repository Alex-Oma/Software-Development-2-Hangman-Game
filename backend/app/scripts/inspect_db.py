# A simple script to inspect the hangman database for debugging purposes.
import sqlite3, pathlib, sys
p = pathlib.Path('backend/app/database/hangman.db')
print('db exists', p.exists(), p)
if not p.exists():
    sys.exit(1)
conn = sqlite3.connect(str(p))
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('tables:', cur.fetchall())
# attempt to fetch rows from Word table if present
candidates = ['word','words','Word','Words']
for t in candidates:
    try:
        cur.execute(f"SELECT text, topic, difficulty FROM {t} LIMIT 5")
        rows = cur.fetchall()
        print(f'rows from {t}:', rows)
    except Exception as e:
        print(f'cannot select from {t}:', e)
conn.close()

