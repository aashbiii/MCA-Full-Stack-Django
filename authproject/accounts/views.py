from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   # Q28
from django.contrib import messages


# ── Q27: Login View ───────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# ── Q27: Logout View ──────────────────────────────────────────
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')


# ── Q28: Protected Views using @login_required ────────────────

@login_required
def dashboard(request):
    """Main dashboard — protected by login_required."""
    return render(request, 'accounts/dashboard.html')


@login_required
def profile(request):
    """User profile page — protected by login_required."""
    return render(request, 'accounts/profile.html')


@login_required
def settings_view(request):
    """Settings page — protected by login_required."""
    return render(request, 'accounts/settings.html')
