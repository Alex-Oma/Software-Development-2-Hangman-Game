#!/usr/bin/env python3
"""Simple migration: add 'guessed' column to game table if missing."""
import sqlite3
from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'database' / 'hangman.db'
print('DB path:', p)
if not p.exists():
    raise SystemExit('DB file not found: ' + str(p))

conn = sqlite3.connect(str(p))
cur = conn.cursor()
cur.execute("PRAGMA table_info('game')")
cols = [r[1] for r in cur.fetchall()]
print('Existing columns:', cols)
if 'guessed' not in cols:
    print('Adding guessed column')
    cur.execute("ALTER TABLE game ADD COLUMN guessed TEXT DEFAULT ''")
    conn.commit()
    cur.execute("PRAGMA table_info('game')")
    print('New columns:', [r[1] for r in cur.fetchall()])
else:
    print('guessed column already present')
conn.close()

