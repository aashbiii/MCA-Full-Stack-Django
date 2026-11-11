from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Registration


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created for @{form.cleaned_data['username']}!")
            return redirect('success')
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = RegistrationForm()

    return render(request, 'validator/register.html', {'form': form})


def success(request):
    registrations = Registration.objects.order_by('-created_at')
    return render(request, 'validator/success.html', {'registrations': registrations})
