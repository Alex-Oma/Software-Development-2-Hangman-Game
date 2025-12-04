from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path

from . import models
from .database import engine
from .routers import auth, games

# create FastAPI app instance
app = FastAPI(title="Hangman Game Backend API")

# mount the frontend static folder using a resolved filesystem path
static_dir = Path(__file__).resolve().parent / "frontend" / "static"
if static_dir.exists():
    # mount static files
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

# include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(games.router, prefix="/api/games", tags=["games"])

# create database tables and seed data on startup
@app.on_event("startup")
def on_startup():
    """Create database tables and seed initial data on startup."""
    # create tables
    try:
        models.SQLModel.metadata.create_all(engine)
    except Exception:
        # best-effort in skeleton - keep startup tolerant
        pass

    # seed demo data (words and a demo user)
    try:
        from .data.seed_words import seed
        from sqlmodel import Session
        from .core import security
        from . import models as _models

        # seed words
        with Session(engine) as session:
            seed(session)
            # ensure demo user exists
            demo = session.exec(__import__('sqlmodel').sqlmodel.sql.select(_models.User).where(_models.User.username == 'demo')).first()
            if not demo:
                # create demo user
                demo_user = _models.User(username='demo', email='demo@example.com', hashed_password=security.get_password_hash('demo'))
                session.add(demo_user)
                session.commit()
    except Exception:
        # ignore seed failures in skeleton
        pass

# root endpoint to redirect to frontend
@app.get("/")
def root():
    # Redirect to the frontend index.html
    return RedirectResponse("/frontend/static/index.html")
