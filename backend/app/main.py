from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path
from contextlib import asynccontextmanager
import logging

from . import models
from .database import engine
from .routers import auth, games


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context: create DB tables and seed data before the app starts."""
    # create tables
    try:
        models.SQLModel.metadata.create_all(engine)
    except Exception:
        # best-effort in skeleton - keep startup tolerant
        pass

    # seed demo data (words and a demo user)
    try:
        from .data.seed_words import seed
        from sqlmodel import Session, select
        from . import models as _models

        # setup logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # run seeding within a session
        with Session(engine) as session:
            try:
                # seed words
                logger.info('Running DB seed from seed_words.seed(...)')
                # call seed function
                seeded = seed(session)
                # log result
                logger.info(f'Seed returned: {seeded} words in DB (seed function result)')
                # verify seed: count words
                try:
                    # query count of words
                    cnt = session.exec(select(_models.Word)).all()
                    # log count
                    logger.info(f'Verified words in DB after seeding: {len(cnt)}')
                except Exception:
                    # log query failure
                    logger.exception('Failed to query Word table after seeding')
            except Exception:
                # log seed function failure
                logger.exception('Seed function raised an exception')
    except Exception:
        # ignore seed failures in skeleton but log
        logging.exception('Failed to run seed on startup')

    # startup complete
    yield



# create FastAPI app instance with lifespan
app = FastAPI(title="Hangman Game Backend API", lifespan=lifespan)

# mount the frontend static folder using a resolved filesystem path
static_dir = Path(__file__).resolve().parent / "frontend" / "static"
# only mount if the directory exists
if static_dir.exists():
    # mount static files at a subpath so API routes are not intercepted
    app.mount("/frontend/static", StaticFiles(directory=str(static_dir), html=True), name="static")

# include API routers
# authentication and game management
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(games.router, prefix="/api/games", tags=["games"])


# root endpoint to redirect to frontend
@app.get("/")
def root():
    '''Root endpoint that redirects to the frontend index.html'''
    # Redirect to the frontend index.html
    return RedirectResponse("/frontend/static/index.html")
