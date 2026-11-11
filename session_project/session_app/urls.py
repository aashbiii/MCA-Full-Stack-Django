from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('add-message/', views.add_message, name='add_message'),
    path('clear-messages/', views.clear_messages, name='clear_messages'),
    path('set-expiry/', views.set_expiry, name='set_expiry'),
]
