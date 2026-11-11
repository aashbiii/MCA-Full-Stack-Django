from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return render(request, 'accounts/admin_dashboard.html')
    elif request.user.groups.filter(name='Manager').exists():
        return render(request, 'accounts/manager_dashboard.html')
    elif request.user.groups.filter(name='Employee').exists():
        return render(request, 'accounts/employee_dashboard.html')
    else:
        return render(request, 'accounts/no_role.html')
