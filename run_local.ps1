# This PowerShell helper script so that I can run the FastAPI app locally
python -m uvicorn backend.app.main:app --reload --port 8000