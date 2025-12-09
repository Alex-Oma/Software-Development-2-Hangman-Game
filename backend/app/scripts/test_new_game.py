from sqlmodel import Session, select
from backend.app.database import engine
from backend.app import models
from backend.app.routers import games
from backend.app.schemas.schemas import GameCreate
from backend.app import crud


def main():
    with Session(engine) as session:
        # ensure demo user exists
        demo = session.exec(select(models.User).where(models.User.username == 'demo')).first()
        if not demo:
            demo = crud.create_user(session, 'demo', 'demo@example.com', 'demo')
        payload = GameCreate(difficulty='easy')
        game = games.new_game(payload, session, current_user=demo)

        # games.new_game now returns a response dict (matching GameRead) for safety
        if isinstance(game, dict):
            print('GAME ID:', game.get('id'))
            print('REVEALED:', game.get('revealed'))
            print('ATTEMPTS_LEFT:', game.get('attempts_left'))
            print('SCORE:', game.get('score'))
            w = game.get('word')
            if w:
                print('WORD meta id:', w.get('id'))
                print('WORD clue:', w.get('clue'))
                print('WORD topic:', w.get('topic'))
                print('WORD difficulty:', w.get('difficulty'))
            else:
                print('No word meta returned')
        else:
            # fallback: older behavior returned ORM object; print attributes safely
            print('GAME ID:', getattr(game, 'id', None))
            print('REVEALED:', getattr(game, 'revealed', None))
            print('ATTEMPTS_LEFT:', getattr(game, 'attempts_left', None))
            print('SCORE:', getattr(game, 'score', None))
            w = getattr(game, 'word', None)
            if w:
                # try meta fields first
                print('WORD meta id:', getattr(w, 'id', None))
                print('WORD clue:', getattr(w, 'clue', None))
                print('WORD topic:', getattr(w, 'topic', None))
                print('WORD difficulty:', getattr(w, 'difficulty', None))
            else:
                print('No nested word attached')


if __name__ == '__main__':
    main()
