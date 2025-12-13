# This PowerShell helper script so that I can run the FastAPI app locally
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000