from django.shortcuts import render
from django.views import View

# Function-Based View
def function_view(request):
    return render(request, 'core/function_view.html')


# Class-Based View
class ClassBasedHelloView(View):
    def get(self, request):
        return render(request, 'core/class_view.html')
