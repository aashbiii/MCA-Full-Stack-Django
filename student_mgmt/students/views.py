from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import Student, Department
from .forms import StudentForm, StudentSearchForm, DepartmentForm


def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    graduated_students = Student.objects.filter(status='graduated').count()
    avg_gpa = Student.objects.aggregate(avg=Avg('gpa'))['avg'] or 0
    departments = Department.objects.annotate(student_count=Count('students'))
    recent_students = Student.objects.select_related('department').order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'graduated_students': graduated_students,
        'avg_gpa': round(avg_gpa, 2),
        'departments': departments,
        'recent_students': recent_students,
    }
    return render(request, 'students/dashboard.html', context)


def student_list(request):
    form = StudentSearchForm(request.GET)
    students = Student.objects.select_related('department').all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        department = form.cleaned_data.get('department')
        status = form.cleaned_data.get('status')

        if query:
            students = students.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(student_id__icontains=query) |
                Q(email__icontains=query)
            )
        if department:
            students = students.filter(department=department)
        if status:
            students = students.filter(status=status)

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_count': students.count(),
    }
    return render(request, 'students/student_list.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.get_full_name()}" created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'action': 'Create',
    })


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.get_full_name()}" updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Edit {student.get_full_name()}',
        'action': 'Update',
    })


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.get_full_name()
        student.delete()
        messages.success(request, f'Student "{name}" deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


def department_list(request):
    departments = Department.objects.annotate(student_count=Count('students')).order_by('name')
    return render(request, 'students/department_list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'students/department_form.html', {
        'form': form, 'title': 'Add Department', 'action': 'Create'
    })


def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" updated!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'students/department_form.html', {
        'form': form, 'dept': dept, 'title': f'Edit {dept.name}', 'action': 'Update'
    })


def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = dept.name
        dept.delete()
        messages.success(request, f'Department "{name}" deleted.')
        return redirect('department_list')
    return render(request, 'students/department_confirm_delete.html', {'dept': dept})
