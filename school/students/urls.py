from django.urls import path
from . import views


urlpatterns = [

    path('', views.fbv_student_list, name='home'),

    path('fbv/',                    views.fbv_student_list,   name='fbv_list'),
    path('fbv/add/',                views.fbv_student_create, name='fbv_create'),
    path('fbv/<int:pk>/',           views.fbv_student_detail, name='fbv_detail'),   # dynamic
    path('fbv/<int:pk>/edit/',      views.fbv_student_edit,   name='fbv_edit'),     # dynamic
    path('fbv/<int:pk>/delete/',    views.fbv_student_delete, name='fbv_delete'),   # dynamic

]
