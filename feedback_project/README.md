# Online Feedback System - Django Lab

A simple online feedback system with database integration using Django's built-in forms.

## Features
- Submit feedback with name, email, category, star rating, subject & message
- Django built-in `ModelForm` with custom widgets
- SQLite database integration
- View all submitted feedback with stats
- Django Admin panel support

## Setup & Run

```bash
# 1. Install Django
pip install django

# 2. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 3. (Optional) Create admin superuser
python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```

## URLs
| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Submit Feedback Form |
| `http://127.0.0.1:8000/success/` | Thank You Page |
| `http://127.0.0.1:8000/feedback/` | View All Feedback |
| `http://127.0.0.1:8000/admin/` | Django Admin |

## Project Structure
```
feedback_project/
├── manage.py
├── requirements.txt
├── feedback_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── feedback/
    ├── models.py      ← Feedback model
    ├── forms.py       ← ModelForm (built-in forms)
    ├── views.py       ← submit, success, list views
    ├── urls.py
    ├── admin.py
    └── templates/feedback/
        ├── submit.html
        ├── success.html
        └── list.html
```
