from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path
from contextlib import asynccontextmanager

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
        from sqlmodel import Session
        from .core import security
        from . import models as _models

        with Session(engine) as session:
            seed(session)
            # ensure demo user exists
            demo = session.exec(__import__('sqlmodel').sqlmodel.sql.select(_models.User).where(_models.User.username == 'demo')).first()
            if not demo:
                demo_user = _models.User(username='demo', email='demo@example.com', hashed_password=security.get_password_hash('demo'))
                session.add(demo_user)
                session.commit()
    except Exception:
        # ignore seed failures in skeleton
        pass

    yield
    # no explicit shutdown actions required for now


# create FastAPI app instance with lifespan
app = FastAPI(title="Hangman Game Backend API", lifespan=lifespan)

# mount the frontend static folder using a resolved filesystem path
static_dir = Path(__file__).resolve().parent / "frontend" / "static"
if static_dir.exists():
    # mount static files at a subpath so API routes are not intercepted
    app.mount("/frontend/static", StaticFiles(directory=str(static_dir), html=True), name="static")

# include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(games.router, prefix="/api/games", tags=["games"])


# root endpoint to redirect to frontend
@app.get("/")
def root():
    # Redirect to the frontend index.html
    return RedirectResponse("/frontend/static/index.html")
