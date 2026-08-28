from app.main import app

# This file exists so that if Railway/Nixpacks defaults to running `uvicorn main:app`
# it will correctly pick up the FastAPI app instance from the app/ folder.
