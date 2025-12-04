# This module was moved into the `backend.app.models` package (a directory).
# Here we keep a lightweight shim and keep imports from failing during refactors.
from .models import User, Word, Game  # re-export for compatibility

__all__ = ["User", "Word", "Game"]
