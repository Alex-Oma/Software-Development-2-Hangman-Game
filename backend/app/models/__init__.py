from sqlmodel import SQLModel, Field, Relationship

from .models import User, Word, Game
from . import models as _models  # keep a reference to the submodule

# Expose models for easier imports
__all__ = ["SQLModel", "Field", "Relationship", "User", "Word", "Game"]
