from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),
    path('success/', views.success, name='success'),
    path('feedback/', views.all_feedback, name='all_feedback'),
]
