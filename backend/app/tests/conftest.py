import sys
from pathlib import Path

# Ensure the repository root is on sys.path so imports like `backend.app` work
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

