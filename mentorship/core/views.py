from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import Profile, Meeting
from .forms import LoginForm, MenteeCreateForm, MenteeEditForm, MeetingForm, MeetingNotesForm


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_mentor():
    p = Profile.objects.filter(role='mentor').first()
    return p.user if p else None


def require_mentor(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
            messages.error(request, "Access denied.")
            return redirect('dashboard')
        return fn(request, *args, **kwargs)
    return wrapper


def require_mentee(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentee':
            messages.error(request, "Access denied.")
            return redirect('dashboard')
        return fn(request, *args, **kwargs)
    return wrapper


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    user    = request.user
    profile = user.profile

    if profile.is_mentor():
        mentees  = Profile.objects.filter(role='mentee').select_related('user')
        # Requests the mentor must respond to = mentee-initiated, still pending
        incoming = Meeting.objects.filter(mentor=user, status='pending', requested_by='mentee')
        # Requests mentor sent that are still pending
        sent_pending = Meeting.objects.filter(mentor=user, status='pending', requested_by='mentor')
        upcoming = Meeting.objects.filter(
            mentor=user, status='accepted', meeting_date__gt=timezone.now()
        ).order_by('meeting_date')[:6]
        past = Meeting.objects.filter(
            mentor=user, meeting_date__lt=timezone.now()
        ).exclude(status='pending').order_by('-meeting_date')[:6]
        return render(request, 'core/mentor_dashboard.html', {
            'mentees': mentees, 'incoming': incoming,
            'sent_pending': sent_pending,
            'upcoming': upcoming, 'past': past,
        })

    else:
        mentor   = get_mentor()
        # Requests mentee must respond to = mentor-initiated, still pending
        incoming = Meeting.objects.filter(mentee=user, status='pending', requested_by='mentor')
        # Requests mentee sent, still pending
        sent_pending = Meeting.objects.filter(mentee=user, status='pending', requested_by='mentee')
        upcoming = Meeting.objects.filter(
            mentee=user, status='accepted', meeting_date__gt=timezone.now()
        ).order_by('meeting_date')[:6]
        past = Meeting.objects.filter(
            mentee=user, meeting_date__lt=timezone.now()
        ).exclude(status='pending').order_by('-meeting_date')[:6]
        return render(request, 'core/mentee_dashboard.html', {
            'mentor': mentor, 'incoming': incoming,
            'sent_pending': sent_pending,
            'upcoming': upcoming, 'past': past,
        })


# ── Mentee CRUD (Mentor only) ─────────────────────────────────────────────────

@require_mentor
def mentee_list(request):
    mentees = Profile.objects.filter(role='mentee').select_related('user')
    return render(request, 'core/mentee_list.html', {'mentees': mentees})


@require_mentor
def mentee_add(request):
    form = MenteeCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f"Student '{user.get_full_name() or user.username}' added!")
        return redirect('mentee_list')
    return render(request, 'core/mentee_form.html', {'form': form, 'action': 'Add'})


@require_mentor
def mentee_edit(request, pk):
    mentee  = get_object_or_404(User, pk=pk, profile__role='mentee')
    p       = mentee.profile
    initial = {
        'first_name': mentee.first_name, 'last_name': mentee.last_name,
        'email': mentee.email, 'bio': p.bio, 'phone': p.phone, 'subject': p.subject,
    }
    form = MenteeEditForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        mentee.first_name = d['first_name']
        mentee.last_name  = d.get('last_name', '')
        mentee.email      = d.get('email', '')
        mentee.save()
        p.bio = d.get('bio', ''); p.phone = d.get('phone', ''); p.subject = d.get('subject', '')
        p.save()
        messages.success(request, "Student updated.")
        return redirect('mentee_list')
    return render(request, 'core/mentee_form.html', {'form': form, 'action': 'Edit', 'mentee': mentee})


@require_mentor
def mentee_view(request, pk):
    mentee   = get_object_or_404(User, pk=pk, profile__role='mentee')
    meetings = Meeting.objects.filter(mentee=mentee).order_by('-meeting_date')
    return render(request, 'core/mentee_detail.html', {'mentee': mentee, 'meetings': meetings})


@require_mentor
def mentee_delete(request, pk):
    mentee = get_object_or_404(User, pk=pk, profile__role='mentee')
    if request.method == 'POST':
        name = mentee.get_full_name() or mentee.username
        mentee.delete()
        messages.success(request, f"Student '{name}' deleted.")
        return redirect('mentee_list')
    return render(request, 'core/mentee_confirm_delete.html', {'mentee': mentee})


# ── Meetings ──────────────────────────────────────────────────────────────────

@require_mentor
def mentor_request_meeting(request, mentee_pk):
    """Mentor sends a meeting request to a mentee."""
    mentee = get_object_or_404(User, pk=mentee_pk, profile__role='mentee')
    form   = MeetingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        m = form.save(commit=False)
        m.mentor = request.user; m.mentee = mentee
        m.requested_by = 'mentor'; m.status = 'pending'
        m.save()
        messages.success(request, f"Meeting request sent to {mentee.get_full_name() or mentee.username}.")
        return redirect('mentee_view', pk=mentee_pk)
    return render(request, 'core/meeting_form.html', {'form': form, 'other': mentee, 'action': 'Request Meeting with'})


@require_mentee
def mentee_request_meeting(request):
    """Mentee sends a meeting request to the mentor."""
    mentor = get_mentor()
    if not mentor:
        messages.error(request, "No mentor found in the system.")
        return redirect('dashboard')
    form = MeetingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        m = form.save(commit=False)
        m.mentor = mentor; m.mentee = request.user
        m.requested_by = 'mentee'; m.status = 'pending'
        m.save()
        messages.success(request, "Meeting request sent!")
        return redirect('dashboard')
    return render(request, 'core/meeting_form.html', {'form': form, 'other': mentor, 'action': 'Request Meeting with'})


@login_required
def meeting_respond(request, pk, action):
    """Accept or decline a meeting — only the recipient can respond."""
    meeting = get_object_or_404(Meeting, pk=pk)
    user    = request.user

    # Validate: only the person who did NOT request can respond
    if meeting.requested_by == 'mentor' and user != meeting.mentee:
        messages.error(request, "Not authorised."); return redirect('dashboard')
    if meeting.requested_by == 'mentee' and user != meeting.mentor:
        messages.error(request, "Not authorised."); return redirect('dashboard')
    if meeting.status != 'pending':
        messages.info(request, "This request has already been responded to.")
        return redirect('dashboard')

    if action == 'accept':
        meeting.status = 'accepted'
        messages.success(request, f"Meeting '{meeting.title}' accepted! ✅")
    elif action == 'decline':
        meeting.status = 'declined'
        messages.info(request, f"Meeting '{meeting.title}' declined.")
    meeting.save()
    return redirect('dashboard')


@login_required
def meeting_complete(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.user not in [meeting.mentor, meeting.mentee]:
        return redirect('dashboard')
    form = MeetingNotesForm(request.POST or None, instance=meeting)
    if request.method == 'POST' and form.is_valid():
        m = form.save(commit=False)
        m.status = 'completed'; m.save()
        messages.success(request, "Meeting marked as completed.")
        return redirect('all_meetings')
    return render(request, 'core/meeting_notes.html', {'form': form, 'meeting': meeting})


@login_required
def meeting_cancel(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.user not in [meeting.mentor, meeting.mentee]:
        return redirect('dashboard')
    if request.method == 'POST':
        meeting.status = 'cancelled'; meeting.save()
        messages.info(request, "Meeting cancelled.")
        return redirect('all_meetings')
    return render(request, 'core/meeting_cancel_confirm.html', {'meeting': meeting})


@login_required
def all_meetings(request):
    user = request.user
    qs   = (Meeting.objects.filter(mentor=user) if user.profile.is_mentor()
            else Meeting.objects.filter(mentee=user))
    return render(request, 'core/all_meetings.html', {'meetings': qs.order_by('-meeting_date')})
