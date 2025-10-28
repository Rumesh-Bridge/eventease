from fastapi import FastAPI
from database import Base, engine
import models
from routers import users  # <-- ADD THIS LINE

app = FastAPI(title="EventEase API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to EventEase API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Database Setup ---
@app.on_event("startup")
def on_startup() -> None:
    # Ensure all tables are created at startup
    models.Base.metadata.create_all(bind=engine)

# --- Include Routers ---
app.include_router(users.router) # <-- This will now work

# --- Run the server ---
if __name__ == "__main__":
    # For local development: python app.py
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)