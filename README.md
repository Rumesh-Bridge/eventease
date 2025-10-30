# 🎟️ EventEase - Event Booking System

**EventEase** is a full-stack event booking and management system built with **Python (FastAPI)** and **Jinja2** for server-side rendering.  
It allows users to browse, book, and manage event reservations — while administrators can efficiently manage events and monitor bookings.  
AI-powered tools are integrated throughout to enhance both user and admin experiences.

---

## ✨ Core Features

### 🧑 User Features
- **Browse Events:** Explore upcoming public events on the main page.
- **Event Details:** View detailed event pages with full descriptions and booking forms.
- **User Authentication:** Secure login and registration using **JWT (JSON Web Tokens)**.
- **Event Booking:** Book one or more seats per event with **real-time seat availability**.
- **My Bookings Dashboard:** View all user bookings in a private dashboard.
- **Booking History:** Filter bookings by **Upcoming** and **Past**.
- **Cancel Booking:** Cancel existing bookings (automatically restores available seats).
- **PDF Confirmation:** Download **PDF booking confirmations** after successful reservations.

---

### 🤖 AI-Powered Features
- **AI Chat Assistant:**  
  A site-wide chatbot that answers event-related questions using real-time data from the database.
- **AI Booking Summary:**  
  Generates natural-language summaries of a user’s upcoming and past events.
- **AI Description Enhancer:**  
  Admins can input a short event prompt — the AI generates a full, professional event description.

---

### 🔑 Admin Features
- **Secure Admin Login:**  
  Dedicated admin login page for enhanced security.
- **Admin Dashboard:**  
  Centralized interface for managing events and bookings.
- **Event Management (CRUD):**  
  Create, read, update, and delete events with ease.
- **Booking Management:**  
  View and manage all user bookings across the platform.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** – Core framework for building the API and serving pages.
- **Uvicorn** – ASGI server.
- **SQLAlchemy** – ORM for database operations.
- **Pydantic** – Data validation and schema management.
- **`python-jose[cryptography]`** – JWT token handling.
- **`passlib[bcrypt]`** – Secure password hashing.
- **`openai`** – AI integrations for assistant, summaries, and content generation.

### Frontend
- **Jinja2 Templates** – Server-side HTML rendering.
- **Bootstrap 5** – Responsive, modern UI.
- **Vanilla JavaScript** – For interactivity (API calls, filtering, etc).

### Database
- **SQLite** – Lightweight and simple to set up.

### Other Libraries
- **`reportlab`** – PDF generation for booking confirmations.
- **`python-dotenv`** – Environment variable management.

---

## 🚀 Setup and Installation

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/eventease.git
cd eventease

# Project Setup and Configuration

This guide will walk you through setting up and running the application.

## 🚀 1. Installation

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate

** macOS / Linux: **
```bash
python -m venv venv
source venv/bin/activate


### 3. Install Dependencies
```bash
pip install -r requirements.txt

## 2. Configuration
### A. Environment Variables
Create a .env file in the project root and add your OpenAI API key:

```bash
OPENAI_API_KEY="sk-YourSecretKeyGoesHere"

### B. Set Your JWT Secret Key
```bash
SECRET_KEY = "your-new-32-byte-random-string-goes-here"

## 🏃 3. Running the Application
```bash
uvicorn app:app --reload

```

- Access the app in your browser at:  
  `http://127.0.0.1:8000`

- Interactive API docs available at:  
  `http://127.0.0.1:8000/docs`

---

## 📦 Directory Structure (Suggested)

```
eventease/
│
├── app.py                  # Main FastAPI app entrypoint
├── ai_utils.py             # AI utility functions (OpenAI integration)
├── cruds/                  # Database CRUD operations
├── routers/                # API route definitions
├── schemas.py              # Pydantic schemas for requests/responses
├── models.py               # SQLAlchemy ORM models
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, JS, images
├── tests/                  # Unit/integration tests
│
├── requirements.txt
├── .env                    # Environment variables (not committed)
└── README.md
```

---

## 🗣️ Usage Tips

- **Booking an event:**  
  Navigate to the home/events page, choose an event, fill in the seat quantity, and book. A PDF confirmation is available after a successful reservation.

- **Admin credentials:**  
  The initial admin user must be created directly in the database, or via a pre-set script (see `cruds/` or contact the maintainer).

- **AI features:**  
  Try interacting with the chatbot for event info or ask for descriptions as an admin during event creation.


## ❓ Troubleshooting

- **Database errors:**  
  Double-check your `.env` and the SQLite file path. If needed, run initial migrations.

- **OpenAI issues:**  
  Ensure your API key is valid and has quota. See `.env` configuration.

- **Cannot start (port in use):**  
  Another process may be using port 8000. Kill unnecessary processes or change the port.

---

## 📋 License

MIT License.

---

*For questions and support, you may open an issue on GitHub or reach out to the maintainer.*