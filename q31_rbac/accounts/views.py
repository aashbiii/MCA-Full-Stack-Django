from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import LoginForm, RegisterForm
from .decorators import admin_required, teacher_required, student_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    role = request.user.role
    if role == 'admin':   return redirect('admin_dashboard')
    if role == 'teacher': return redirect('teacher_dashboard')
    return redirect('student_dashboard')


@admin_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    context = {
        'users':    users.order_by('role', 'username'),
        'admins':   users.filter(role='admin').count(),
        'teachers': users.filter(role='teacher').count(),
        'students': users.filter(role='student').count(),
        'total':    users.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@teacher_required
def teacher_dashboard(request):
    students = CustomUser.objects.filter(role='student')
    context = {
        'students': students,
        'total_students': students.count(),
        'courses': ['Mathematics', 'Physics', 'Computer Science', 'English'],
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@student_required
def student_dashboard(request):
    context = {
        'teachers': CustomUser.objects.filter(role='teacher'),
        'subjects': [
            {'name': 'Mathematics',      'grade': 'A',  'progress': 85},
            {'name': 'Physics',          'grade': 'B+', 'progress': 72},
            {'name': 'Computer Science', 'grade': 'A+', 'progress': 95},
            {'name': 'English',          'grade': 'B',  'progress': 68},
        ],
    }
    return render(request, 'accounts/student_dashboard.html', context)


@admin_required
def manage_users(request):
    users = CustomUser.objects.all().order_by('role', 'username')
    return render(request, 'accounts/manage_users.html', {'users': users})


@admin_required
def delete_user(request, pk):
    if request.method == 'POST':
        try:
            u = CustomUser.objects.get(pk=pk)
            if u != request.user:
                u.delete()
                messages.success(request, 'User deleted.')
            else:
                messages.error(request, 'Cannot delete your own account.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
    return redirect('manage_users')
