from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import identify_hasher
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .models import UserProfile, LoginLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# ── Register ──────────────────────────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Create profile
        initials = (user.first_name[:1] + user.last_name[:1]).upper() or user.username[:2].upper()
        UserProfile.objects.create(user=user, avatar_initial=initials)
        messages.success(request, "Account created! Please log in.")
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


# ── Login ─────────────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')[:200]

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Update profile login stats
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.login_count += 1
            profile.last_login_ip = ip
            profile.save()

            # Log success
            LoginLog.objects.create(user=user, ip_address=ip, user_agent=ua, success=True)

            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            # Attempt to log failed login
            from django.contrib.auth.models import User
            username = request.POST.get('username', '')
            try:
                failed_user = User.objects.get(username=username)
                LoginLog.objects.create(user=failed_user, ip_address=ip, user_agent=ua, success=False)
            except User.DoesNotExist:
                pass

    return render(request, 'accounts/login.html', {'form': form})


# ── Logout ────────────────────────────────────────────────────────────────────
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    user    = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]
    logs    = LoginLog.objects.filter(user=user)[:8]

    # Show the hashed password algorithm info
    hasher = identify_hasher(user.password)
    hash_info = {
        'algorithm': hasher.algorithm,
        'hash_preview': user.password[:60] + '…',
    }

    return render(request, 'accounts/dashboard.html', {
        'profile':   profile,
        'logs':      logs,
        'hash_info': hash_info,
    })


# ── Change Password ───────────────────────────────────────────────────────────
@login_required
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Keep session alive after password change
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully!")
        return redirect('dashboard')

    return render(request, 'accounts/change_password.html', {'form': form})
