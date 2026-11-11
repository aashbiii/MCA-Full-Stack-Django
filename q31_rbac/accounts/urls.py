from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.dashboard,          name='home'),
    path('login/',              views.login_view,         name='login'),
    path('register/',           views.register_view,      name='register'),
    path('logout/',             views.logout_view,        name='logout'),
    path('dashboard/',          views.dashboard,          name='dashboard'),
    path('dashboard/admin/',    views.admin_dashboard,    name='admin_dashboard'),
    path('dashboard/teacher/',  views.teacher_dashboard,  name='teacher_dashboard'),
    path('dashboard/student/',  views.student_dashboard,  name='student_dashboard'),
    path('users/',              views.manage_users,       name='manage_users'),
    path('users/<int:pk>/delete/', views.delete_user,     name='delete_user'),
]
