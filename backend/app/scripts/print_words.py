#!/usr/bin/env python3
"""
Utility to list all words from the project's SQLite database.
Prints: text (or word/name), topic and difficulty for each row when possible.
Also prints available tables and columns to help debugging.
"""
from pathlib import Path
import sqlite3
import sys

# Compute DB path relative to this script: ../database/hangman.db
db_path = Path(__file__).resolve().parent.parent / 'database' / 'hangman.db'
print(f'Using database file: {db_path}')
if not db_path.exists():
    print('ERROR: database file not found at', db_path, file=sys.stderr)
    sys.exit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

# List available tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('Tables in DB:', tables)
if not tables:
    print('No tables found in the database.')
    conn.close()
    sys.exit(0)

# Gather table column info
table_columns = {}
for t in tables:
    cur.execute(f"PRAGMA table_info('{t}')")
    cols = [r[1] for r in cur.fetchall()]
    table_columns[t] = cols
    print(f"  {t}: columns={cols}")

# Candidate sets of column names to try when selecting words
candidate_sets = [
    ('text','topic','difficulty'),
    ('word','topic','difficulty'),
    ('name','topic','difficulty'),
    ('text','clue','topic','difficulty'),
    ('text','clue','difficulty'),
]

found_any = False
for t, cols in table_columns.items():
    for cand in candidate_sets:
        if all(c in cols for c in cand):
            found_any = True
            # Build select list preserving available columns
            select_cols = ', '.join(cand)
            print(f"\nSelecting from {t} columns: {select_cols}")
            try:
                cur.execute(f"SELECT {select_cols} FROM \"{t}\"")
                rows = cur.fetchall()
            except Exception as e:
                print('  Query failed:', e)
                continue
            if not rows:
                print(f'  No rows in table {t} for columns {cand}')
            else:
                for row in rows:
                    # We print sensible mapping
                    mapping = dict(zip(cand, row))
                    text = mapping.get('text') or mapping.get('word') or mapping.get('name')
                    topic = mapping.get('topic')
                    difficulty = mapping.get('difficulty')
                    clue = mapping.get('clue')
                    out = f"- text: {text}"
                    if topic is not None:
                        out += f" | topic: {topic}"
                    if difficulty is not None:
                        out += f" | difficulty: {difficulty}"
                    if clue is not None and 'clue' in cand:
                        out += f" | clue: {clue}"
                    print(out)
            # once we found a matching candidate for this table, stop trying other candidates for same table
            break

if not found_any:
    print('\nCould not find a table with expected word columns. You can inspect the above table/column listing to pick a table and columns to query manually.')

conn.close()
