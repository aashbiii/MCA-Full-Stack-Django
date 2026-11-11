# 🎓 EduTrack — Student Management System

A full-featured Django student management system with CRUD operations and a sleek dark-themed UI.

---

## ✨ Features

- **Dashboard** — Live stats (total students, active, graduated, avg GPA) + recent enrollments
- **Students CRUD** — Create, Read, Update, Delete students with full form validation
- **Department CRUD** — Manage academic departments
- **Search & Filter** — Search by name/ID/email, filter by department and status
- **Pagination** — 10 students per page
- **GPA Tracker** — Visual progress bar per student
- **Status Badges** — Active / Inactive / Graduated / Suspended
- **Django Forms** — Built-in form validation with error display
- **Flash Messages** — Success/error feedback after every action

---

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

### 3. (Optional) Create Superuser for Admin Panel

```bash
python manage.py createsuperuser
```

### 4. (Optional) Load Sample Data

```bash
python manage.py shell < sample_data.py
```

### 5. Run the Server

```bash
python manage.py runserver
```

Open → **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
student_mgmt/
├── manage.py
├── requirements.txt
├── student_mgmt/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── students/
    ├── models.py          # Student & Department models
    ├── views.py           # All CRUD views
    ├── forms.py           # Django forms
    ├── urls.py            # URL routing
    ├── admin.py           # Admin registration
    ├── migrations/
    └── templates/students/
        ├── base.html              # Sidebar layout + styles
        ├── dashboard.html         # Stats overview
        ├── student_list.html      # Table + search
        ├── student_detail.html    # Profile view
        ├── student_form.html      # Create/Edit form
        ├── student_confirm_delete.html
        ├── department_list.html
        ├── department_form.html
        └── department_confirm_delete.html
```

---

## 🗺️ URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | dashboard | Stats overview |
| `/students/` | student_list | Searchable student table |
| `/students/new/` | student_create | Add new student |
| `/students/<id>/` | student_detail | Student profile |
| `/students/<id>/edit/` | student_update | Edit student |
| `/students/<id>/delete/` | student_delete | Delete student |
| `/departments/` | department_list | Department table |
| `/departments/new/` | department_create | Add department |
| `/departments/<id>/edit/` | department_update | Edit department |
| `/departments/<id>/delete/` | department_delete | Delete department |
| `/admin/` | Django Admin | Full admin panel |

---

## 🎨 Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, swap for PostgreSQL in production)
- **Forms**: Django built-in ModelForms
- **Fonts**: Syne (headings) + DM Sans (body) via Google Fonts
- **Styling**: Custom CSS with dark theme, no external UI frameworks
