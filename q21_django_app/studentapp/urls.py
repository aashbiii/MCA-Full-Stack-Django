from django.urls import path
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('',          views.home,         name='home'),
    path('students/', views.student_list, name='student_list'),
    path('about/',    views.about,        name='about'),
]
