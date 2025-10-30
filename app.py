from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from cruds import event_crud
from database import Base, engine
import models
from routers import users, events, bookins
from fastapi.staticfiles import StaticFiles
from database import Base, engine, get_db

app = FastAPI(title="EventEase API", version="0.1.0")

# ---  Mount your 'static' folder ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Set up Jinja2 templates ---
templates = Jinja2Templates(directory="templates")



# ---  API root ---
@app.get("/api/", include_in_schema=False)
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
app.include_router(users.router) 
app.include_router(events.router)
app.include_router(bookins.router)


# --- Create the Home Page Route ---
@app.get("/", include_in_schema=False) 
def read_home(request: Request, db: Session = Depends(get_db)):
    """
    Serves the home.html page.
    """
    events = event_crud.get_events(db, skip=0, limit=6)
    # Pass the events to the template
    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "events": events} # Add events to context
    )


@app.get("/users/login/", include_in_schema=False)
def get_login_page(request: Request):
    """
    Serves the login.html page.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/users/register/", include_in_schema=False)
def get_register_page(request: Request):
    """
    Serves the register.html page.
    """
    return templates.TemplateResponse("register.html", {"request": request})
    
# --- Run the server ---
if __name__ == "__main__":
    # For local development: python app.py
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)