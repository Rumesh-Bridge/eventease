from fastapi import Depends, FastAPI, HTTPException, Request, status
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

@app.get("/events/{event_id}", include_in_schema=False)
def get_event_detail_page(request: Request, event_id: int, db: Session = Depends(get_db)):
    """Serves the event_detail.html page for a single event."""
    event = event_crud.get_event(db, event_id=event_id)
    if not event:
      
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return templates.TemplateResponse("event_detail.html", {"request": request, "event": event})

@app.get("/bookings/me",include_in_schema=False)
def get_my_bookings_page(request:Request):
    """ Server the my_bookings_page """

    return templates.TemplateResponse("my_booking.html",{"request":request})

# === ADMIN SCREEN ====
@app.get("/admin/login", include_in_schema=False)
def get_admin_login_page(request: Request):
    """ Server the admin login page """

    return templates.TemplateResponse("admin/admin_login.html",{"request":request})

@app.get("/admin/dashboard", include_in_schema=False)
def get_admin_login_page(request: Request):
    """ Server the admin dashbaord page """

    return templates.TemplateResponse("admin/admin_dashboard.html",{"request":request})

@app.get("/admin/events/new/", include_in_schema=False)
def get_create_event_page(request: Request):
    """
    Serves the page for creating a new event.
    """
    return templates.TemplateResponse("admin/create_event.html", {"request": request})   

# --- Run the server ---
if __name__ == "__main__":
    # For local development: python app.py
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)