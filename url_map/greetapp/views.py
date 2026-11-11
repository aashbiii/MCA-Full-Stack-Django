from django.shortcuts import render

def greet(request, name):
    return render(request, 'greetapp/greeting.html', {'name': name})
