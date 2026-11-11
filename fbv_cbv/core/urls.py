from django.urls import path
from .views import function_view, ClassBasedHelloView

urlpatterns = [
    path('function/', function_view, name='function_view'),
    path('class/', ClassBasedHelloView.as_view(), name='class_view'),
]
