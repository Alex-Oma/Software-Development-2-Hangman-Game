from sqlmodel import Session, select
from .. import models
from ..core import security
from sqlalchemy import func
import logging


def get_user_by_username(session: Session, username: str):
    '''
    Get a user by their username.
    :param session: Session
    :param username: str
    :return: User or None
    '''
    return session.exec(select(models.User).where(models.User.username == username)).first()


def create_user(session: Session, username: str, email: str, password: str):
    '''
    Create a new user with the given username, email, and password.
    :param session: Session
    :param username: str
    :param email: str
    :param password: str
    :return: User
    '''
    hashed = security.get_password_hash(password)
    user = models.User(username=username, email=email, hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_game(session: Session, user: models.User, word: models.Word, initial_attempts: int = 6):
    '''
    Create a new game for the given user and word.
    :param session: Session
    :param user: models.User
    :param word: models.Word
    :param initial_attempts: int
    :return: models.Game
    '''
    game = models.Game(
        user_id=user.id,
        word_id=word.id,
        revealed="_" * len(word.text),
        initial_attempts=initial_attempts,
        attempts_left=initial_attempts
    )
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


def get_random_word(session: Session, topic: str = None, difficulty: str = None):
    '''
    Get a random word, optionally filtered by topic and difficulty.
    :param session: Session
    :param topic: str
    :param difficulty: str
    :return: models.Word or None
    '''

    # Adding logging for debugging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Fetching random word with topic={topic} and difficulty={difficulty}")

    q = select(models.Word)
    if topic:
        q = q.where(models.Word.topic == topic)
    if difficulty:
        q = q.where(models.Word.difficulty == difficulty)

    # Order randomly and limit to 1 to fetch a random matching word
    q = q.order_by(func.random()).limit(1)
    # Execute the query
    word = session.exec(q).first()

    # Log the result
    if not word:
        logger.warning("No matching word found")
        return None
    else:
        logger.info(f"Found word: {word.text} (topic={word.topic}, difficulty={word.difficulty})")

    # Return the found word
    return word

def get_count_of_words(session: Session, topic: str = None, difficulty: str = None):
    '''
    Get the count of words, optionally filtered by topic and difficulty.
    :param session: Session
    :param topic: str
    :param difficulty: str
    :return: int
    '''

    q = select(func.count(models.Word.id))
    if topic:
        q = q.where(models.Word.topic == topic)
    if difficulty:
        q = q.where(models.Word.difficulty == difficulty)

    count = session.exec(q).one()
    return count