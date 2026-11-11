from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Mentee CRUD
    path('students/', views.mentee_list, name='mentee_list'),
    path('students/add/', views.mentee_add, name='mentee_add'),
    path('students/<int:pk>/', views.mentee_view, name='mentee_view'),
    path('students/<int:pk>/edit/', views.mentee_edit, name='mentee_edit'),
    path('students/<int:pk>/delete/', views.mentee_delete, name='mentee_delete'),

    # Meetings
    path('meetings/', views.all_meetings, name='all_meetings'),
    path('meetings/request/<int:mentee_pk>/', views.mentor_request_meeting, name='mentor_request_meeting'),
    path('meetings/request/', views.mentee_request_meeting, name='mentee_request_meeting'),
    path('meetings/<int:pk>/respond/<str:action>/', views.meeting_respond, name='meeting_respond'),
    path('meetings/<int:pk>/complete/', views.meeting_complete, name='meeting_complete'),
    path('meetings/<int:pk>/cancel/', views.meeting_cancel, name='meeting_cancel'),
]
