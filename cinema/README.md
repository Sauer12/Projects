# Cinema Reservation App (MVP)

A simple Django-based cinema reservation system that allows users to book seats for specific movie screenings.  
The MVP version focuses on basic CRUD operations and a convenient admin interface for managing movies, screenings, and reservations.

## Features
- 🎬 Manage movies and screening halls
- 🪑 Reserve one or multiple seats for a chosen screening
- 📅 View screenings per hall
- 🛠 Django Admin with full CRUD support for all models
- 📊 Reservation overview (including seats)

## Tech Stack
- Python 3.x
- Django 4.x
- SQLite (default, can be replaced with PostgreSQL/MySQL)
- HTML/CSS for basic styling

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>

2. **Create and activate a virtual environment**
     ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install dependencies**
     ```bash
    pip install -r requirements.txt

4. **Run migrations**
   ```bash
   python manage.py migrate

5. **Create a superuser for Django Admin**
    ```bash
    python manage.py createsuperuser

6. **Run the development server**
    ```bash
    python manage.py runserver

**Project Structure**
```bash
    cinema/
        ├── admin.py          # Admin interface configuration
        ├── apps.py           # App configuration
        ├── models.py         # Database models
        ├── signals.py        # Signal handlers (if used)
        ├── views.py          # Views for handling requests
        └── templates/        # HTML templates
