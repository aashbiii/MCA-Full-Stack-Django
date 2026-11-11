from django.shortcuts import render, get_object_or_404, redirect
from .models import Student


def fbv_student_list(request):
    """FBV — List all students."""
    students = Student.objects.all()
    return render(request, 'students/fbv_list.html', {'students': students})


def fbv_student_detail(request, pk):
    """FBV — Show a single student by primary key (dynamic URL)."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/fbv_detail.html', {'student': student})


def fbv_student_create(request):
    """FBV — Create a new student."""
    if request.method == 'POST':
        Student.objects.create(
            name    = request.POST['name'],
            roll_no = request.POST['roll_no'],
            branch  = request.POST['branch'],
            year    = request.POST['year'],
            email   = request.POST.get('email', ''),
            phone   = request.POST.get('phone', ''),
        )
        return redirect('fbv_list')
    return render(request, 'students/fbv_form.html', {'action': 'Add', 'view_type': 'FBV'})


def fbv_student_edit(request, pk):
    """FBV — Edit an existing student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.name    = request.POST['name']
        student.roll_no = request.POST['roll_no']
        student.branch  = request.POST['branch']
        student.year    = request.POST['year']
        student.email   = request.POST.get('email', '')
        student.phone   = request.POST.get('phone', '')
        student.save()
        return redirect('fbv_list')
    return render(request, 'students/fbv_form.html', {'student': student, 'action': 'Edit', 'view_type': 'FBV'})


def fbv_student_delete(request, pk):
    """FBV — Delete a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('fbv_list')
    return render(request, 'students/fbv_confirm_delete.html', {'student': student, 'view_type': 'FBV'})
