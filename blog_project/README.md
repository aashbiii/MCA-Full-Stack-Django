# Blog Application — Django Lab (No Database)

A clean blog application built with Django using **in-memory data** (no database required).

## Features
- 📰 Blog post listing with card grid layout
- 🔍 Search by title/excerpt
- 🏷️ Filter by category
- 📖 Full post detail page with related posts
- 👤 About page with author stats
- ✨ Beautiful dark UI — no database needed

## How to Run

```bash
# 1. Install Django
pip install django

# 2. Run server directly (no migrations needed!)
python manage.py runserver
```

## URLs
| URL | Page |
|-----|------|
| `http://127.0.0.1:8000/` | Home — All Posts |
| `http://127.0.0.1:8000/?category=Programming` | Filter by Category |
| `http://127.0.0.1:8000/?search=python` | Search Posts |
| `http://127.0.0.1:8000/post/<slug>/` | Post Detail |
| `http://127.0.0.1:8000/about/` | About Page |

## Project Structure
```
blog_project/
├── manage.py
├── requirements.txt
├── blog_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── blog/
    ├── views.py      ← All data (POSTS list) + all views
    ├── urls.py
    └── templates/blog/
        ├── home.html     ← Post listing + search + filter
        ├── detail.html   ← Full post view
        └── about.html    ← About + author stats
```

## Note on "No Database"
All blog data is stored as a Python list of dictionaries (`POSTS`) inside `views.py`.
No `models.py`, no `migrations/`, no `db.sqlite3` — just pure Django views and templates.
