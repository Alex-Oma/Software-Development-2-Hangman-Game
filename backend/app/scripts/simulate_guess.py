from sqlmodel import Session, select
from backend.app.database import engine
from backend.app import models
from backend.app import crud
from backend.app.routers import games
from backend.app.schemas import schemas

def main():
    with Session(engine) as session:
        # ensure demo user exists
        demo = session.exec(select(models.User).where(models.User.username == 'demo')).first()
        if not demo:
            demo = crud.create_user(session, 'demo', 'demo@example.com', 'demo')
        # pick any word
        word = session.exec(select(models.Word)).first()
        if not word:
            print('No words in DB to test')
            return
        # create game for demo user
        game = crud.create_game(session, demo, word)
        print('Created game id', game.id, 'revealed', game.revealed)
        # First guess - pick first letter of the word
        letter = word.text[0].lower()
        print('Guessing letter', letter)
        payload = schemas.GuessIn(letter=letter)
        try:
            resp = games.guess(game.id, payload, session)
            print('First guess response attempts_left=', resp['attempts_left'], 'score=', resp['score'], 'guessed=', resp.get('guessed'))
        except Exception as e:
            print('First guess raised', type(e), e)
        # Second guess same letter
        try:
            resp2 = games.guess(game.id, payload, session)
            print('Second guess response', resp2)
        except Exception as e:
            print('Second guess raised', type(e), getattr(e, 'status_code', None), getattr(e, 'detail', str(e)))

if __name__ == '__main__':
    main()

