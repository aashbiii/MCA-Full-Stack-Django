"""
Q23 — CRUD Operations using Django ORM
Run this script after migrations:
    python orm_demo.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from students.models import Student

print("\n" + "="*50)
print("  Q23: Django ORM — CRUD Operations")
print("="*50)

# ── CREATE ────────────────────────────────────────
print("\n[CREATE] Adding students...")
Student.objects.all().delete()   # clean slate each run

students_data = [
    dict(name="Arjun Menon",  roll_no="CS001", branch="CSE", year=3, email="arjun@mail.com",  phone="9876543210"),
    dict(name="Priya Nair",   roll_no="CS002", branch="CSE", year=2, email="priya@mail.com",  phone="9876543211"),
    dict(name="Rahul Das",    roll_no="EC001", branch="ECE", year=3, email="rahul@mail.com",  phone="9876543212"),
    dict(name="Sneha Thomas", roll_no="ME001", branch="ME",  year=1, email="sneha@mail.com",  phone="9876543213"),
    dict(name="Arun Kumar",   roll_no="CS003", branch="CSE", year=4, email="arun@mail.com",   phone="9876543214"),
]

for s in students_data:
    obj = Student.objects.create(**s)
    print(f"  Created: {obj}")

# ── READ ──────────────────────────────────────────
print("\n[READ] All students:")
for s in Student.objects.all():
    print(f"  {s.roll_no} | {s.name} | {s.branch} | Year {s.year}")

print("\n[READ] Filter — CSE branch only:")
for s in Student.objects.filter(branch="CSE"):
    print(f"  {s.name}")

print("\n[READ] Get single — CS001:")
s = Student.objects.get(roll_no="CS001")
print(f"  Found: {s.name}, Email: {s.email}")

# ── UPDATE ────────────────────────────────────────
print("\n[UPDATE] Update Arjun Menon's year to 4...")
Student.objects.filter(roll_no="CS001").update(year=4)
s = Student.objects.get(roll_no="CS001")
print(f"  Updated: {s.name} is now in Year {s.year}")

# ── DELETE ────────────────────────────────────────
print("\n[DELETE] Delete ME001...")
Student.objects.filter(roll_no="ME001").delete()
print(f"  Remaining count: {Student.objects.count()}")

print("\n" + "="*50)
print("  CRUD Demo complete!")
print("="*50 + "\n")
