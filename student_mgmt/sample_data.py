"""
Run with: python manage.py shell < sample_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_mgmt.settings')

from students.models import Department, Student
from datetime import date

# Departments
depts = [
    ('Computer Science', 'CS'),
    ('Mathematics', 'MATH'),
    ('Physics', 'PHY'),
    ('Business Administration', 'BUS'),
    ('English Literature', 'ENG'),
]

dept_objs = {}
for name, code in depts:
    d, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
    dept_objs[code] = d
    print(f"Created department: {name}")

# Students
students = [
    ('STU2024001', 'Alice', 'Johnson', 'alice@edu.com', 'F', date(2002, 3, 15), 'CS', 3.85, 'active'),
    ('STU2024002', 'Bob', 'Smith', 'bob@edu.com', 'M', date(2001, 7, 22), 'MATH', 3.42, 'active'),
    ('STU2024003', 'Carol', 'Davis', 'carol@edu.com', 'F', date(2003, 1, 8), 'PHY', 3.90, 'active'),
    ('STU2024004', 'David', 'Wilson', 'david@edu.com', 'M', date(2000, 11, 5), 'BUS', 2.78, 'inactive'),
    ('STU2024005', 'Emma', 'Brown', 'emma@edu.com', 'F', date(2001, 5, 19), 'ENG', 3.65, 'active'),
    ('STU2023001', 'Frank', 'Miller', 'frank@edu.com', 'M', date(1999, 9, 30), 'CS', 3.10, 'graduated'),
    ('STU2024006', 'Grace', 'Taylor', 'grace@edu.com', 'F', date(2002, 12, 14), 'MATH', 3.55, 'active'),
    ('STU2024007', 'Henry', 'Anderson', 'henry@edu.com', 'M', date(2001, 4, 27), 'BUS', 2.95, 'suspended'),
]

for sid, fn, ln, email, gender, dob, dept_code, gpa, status in students:
    s, created = Student.objects.get_or_create(
        student_id=sid,
        defaults={
            'first_name': fn,
            'last_name': ln,
            'email': email,
            'gender': gender,
            'date_of_birth': dob,
            'department': dept_objs[dept_code],
            'gpa': gpa,
            'status': status,
            'phone': '+1 555 000 0001',
            'address': '123 Campus Drive, University City',
        }
    )
    if created:
        print(f"Created student: {fn} {ln}")

print("\n✅ Sample data loaded successfully!")
print(f"   Departments: {Department.objects.count()}")
print(f"   Students: {Student.objects.count()}")
