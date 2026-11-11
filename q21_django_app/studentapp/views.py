from django.shortcuts import render

from .models import Student

def home(request):
    students = Student.objects.all()
    return render(request, 'studentapp/home.html', {
        'app_name': 'Student Application',
        'description': 'A Django app to manage student records.',
        'total': students.count(),
    })

def student_list(request):
    students = Student.objects.all()
    return render(request, 'studentapp/student_list.html', {'students': students})

def about(request):
    return render(request, 'studentapp/about.html', {
        'project': 'myproject',
        'app': 'studentapp',
        'tech': ['Python 3', 'Django 4', 'SQLite3', 'HTML5/CSS3'],
    })
