import pytest
from sqlmodel import SQLModel, create_engine, Session

from backend.app import crud
from backend.app.models import Word

# Fixture to provide an in-memory database session for testing
@pytest.fixture
def in_memory_session():
    # Use an in-memory SQLite database for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Test cases for get_random_word function
def test_get_random_word_no_filters(in_memory_session):
    s = in_memory_session
    # insert sample words
    words = [
        Word(text="apple", clue="A fruit", topic="food", difficulty="easy"),
        Word(text="python", clue="language", topic="tech", difficulty="medium"),
        Word(text="nebula", clue="space cloud", topic="space", difficulty="medium"),
    ]
    for w in words:
        s.add(w)
    s.commit()

    # should return a Word (any)
    res = crud.get_random_word(s)
    assert res is not None
    assert isinstance(res, Word)

# Test with topic and difficulty filters
def test_get_random_word_with_topic_and_difficulty(in_memory_session):
    s = in_memory_session
    # insert sample words
    words = [
        Word(text="apple", clue="A fruit", topic="food", difficulty="easy"),
        Word(text="banana", clue="A fruit", topic="food", difficulty="easy"),
        Word(text="python", clue="language", topic="tech", difficulty="medium"),
        Word(text="raspberry", clue="berry", topic="food", difficulty="hard"),
    ]
    for w in words:
        s.add(w)
    s.commit()

    # Filter by topic=food, difficulty=easy -> should return either apple or banana
    res = crud.get_random_word(s, topic="food", difficulty="easy")
    assert res is not None
    assert res.topic == "food"
    assert res.difficulty == "easy"
    assert res.text in {"apple", "banana"}

    # Filter by topic with no matching difficulty -> should return None
    res_none = crud.get_random_word(s, topic="tech", difficulty="easy")
    assert res_none is None

# Test with only topic filter
def test_get_random_word_difficulty_only(in_memory_session):
    s = in_memory_session
    words = [
        Word(text="a", clue="a", topic="x", difficulty="hard"),
        Word(text="b", clue="b", topic="y", difficulty="medium"),
    ]
    for w in words:
        s.add(w)
    s.commit()

    res = crud.get_random_word(s, difficulty="hard")
    assert res is not None
    assert res.difficulty == "hard"

