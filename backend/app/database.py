from pathlib import Path
from sqlmodel import create_engine

# Place the sqlite DB inside backend/app/database/hangman.db (create folder if missing)
_db_dir = Path(__file__).resolve().parent / "database"
_db_dir.mkdir(parents=True, exist_ok=True)
_db_path = _db_dir / "hangman.db"

# sqlite URL must use forward slashes; use as_posix()
DATABASE_URL = f"sqlite:///{_db_path.as_posix()}"

# create engine; disable echo by default
engine = create_engine(DATABASE_URL, echo=False)
