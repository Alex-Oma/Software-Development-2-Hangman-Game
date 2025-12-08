# This file contains seed data for words to be used in the application.
from pathlib import Path
import json
import logging

# Let's load words from words.json. If loading fails, fall back to a small default list.
_words_file = Path(__file__).resolve().parent / "words.json"
try:
    with _words_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            WORDS = data
        else:
            logging.warning("%s does not contain a JSON list; using default WORDS.", _words_file)
            WORDS = [
                {"text": "apple", "clue": "A fruit", "topic": "food", "difficulty": "easy"},
                {"text": "train", "clue": "A vehicle", "topic": "transport", "difficulty": "easy"},
                {"text": "python", "clue": "A programming language or snake", "topic": "tech", "difficulty": "medium"},
            ]
except FileNotFoundError:
    logging.warning("words.json not found at %s; using default WORDS.", _words_file)
    WORDS = [
        {"text": "apple", "clue": "A fruit", "topic": "food", "difficulty": "easy"},
        {"text": "train", "clue": "A vehicle", "topic": "transport", "difficulty": "easy"},
        {"text": "python", "clue": "A programming language or snake", "topic": "tech", "difficulty": "medium"},
    ]
except Exception as e:
    logging.exception("Failed to load words.json (%s); using default WORDS.", e)
    WORDS = [
        {"text": "apple", "clue": "A fruit", "topic": "food", "difficulty": "easy"},
        {"text": "train", "clue": "A vehicle", "topic": "transport", "difficulty": "easy"},
        {"text": "python", "clue": "A programming language or snake", "topic": "tech", "difficulty": "medium"},
    ]


# Seed function to populate the database with initial words
def seed(session):
    '''
    Seed the database with initial words.
    :param session: Database session
    :return: None
    '''
    # Importing here to avoid circular imports
    from ..models import Word
    from sqlmodel import select
    from sqlalchemy import func

    # Adding logging for debugging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Logging the count of WORDS to be added
    logger.debug(f"Number of words to seed: {len(WORDS)}")

    logger.debug("Seeding words into the database.")

    # Iterate over the WORDS list and add each word to the database
    countWordsAdded = 0
    for w in WORDS:
        # Check if the word already exists
        exists = session.exec(select(Word).where(Word.text == w['text'])).first()
        if not exists:
            # Add the word if it does not already exist
            session.add(Word(text=w.get('text'), clue=w.get('clue'), topic=w.get('topic'), difficulty=w.get('difficulty')))
            countWordsAdded += 1

    # Log the number of words added
    logger.debug(f"Added {countWordsAdded} new words to the database.")

    # Commit the session to save changes
    session.commit()

    # Getting total count of words after seeding
    try:
        total_count = session.exec(select(func.count(Word.id))).scalar_one()
    except Exception:
        # fallback: load all words and count
        total_count = len(session.exec(select(Word)).all())
    logger.debug(f"Total words in database after seeding: {total_count}")
    return total_count
