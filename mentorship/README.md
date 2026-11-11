<<<<<<< HEAD
<<<<<<< HEAD
# MentorSpace
=======
=======
>>>>>>> aa76e4078c8baf718e08f540ee13285acb083b77
# MentorSpace — Django Mentorship Platform

## Quick Start (Local)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Visit http://127.0.0.1:8000

## Demo Accounts
| Role   | Username | Password  |
|--------|----------|-----------|
| Mentor | mentor   | mentor123 |
| Mentee | mentee1  | mentee123 |
| Mentee | mentee2  | mentee123 |
| Mentee | mentee3  | mentee123 |

## Deploy to Render.com (Free)
1. Push this project to a GitHub repo
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Render auto-reads `render.yaml` → provisions PostgreSQL + gunicorn automatically
5. Click **Deploy** ✅

## Features
- Single login page, automatic role-based redirect (mentor / mentee)
- **Mentor Dashboard:** stats overview, incoming student requests with Accept/Decline, upcoming meetings, meeting history, student sidebar
- **Mentee Dashboard:** incoming mentor invitations with Accept/Decline, sent pending requests, upcoming meetings, mentor profile card
- **Mentee CRUD:** Add / View / Edit / Delete students (mentor only)
- **Meeting fields:** Title, Date & Time, Description/Notes
- **Meeting flow:** Either party requests → other party accepts or declines → attended → marked complete with notes
- **Full meeting history** visible to both parties with status badges
- Beautiful dark UI with sidebar navigation
- Render.com deployment ready with PostgreSQL + gunicorn + WhiteNoise
<<<<<<< HEAD
>>>>>>> aa76e40 (Initial commit)
=======
>>>>>>> aa76e4078c8baf718e08f540ee13285acb083b77
