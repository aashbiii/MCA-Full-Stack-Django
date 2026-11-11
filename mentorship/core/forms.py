from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Meeting


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'fi', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'fi'})
    )


class MenteeCreateForm(forms.Form):
    first_name = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class': 'fi', 'placeholder': 'First name'}))
    last_name  = forms.CharField(max_length=50,  required=False, widget=forms.TextInput(attrs={'class': 'fi', 'placeholder': 'Last name'}))
    username   = forms.CharField(max_length=30,  widget=forms.TextInput(attrs={'class': 'fi', 'placeholder': 'username'}))
    email      = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'fi', 'placeholder': 'email@example.com'}))
    password   = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fi', 'placeholder': 'Set password'}))
    subject    = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'fi', 'placeholder': 'e.g. Computer Science'}))
    phone      = forms.CharField(max_length=20,  required=False, widget=forms.TextInput(attrs={'class': 'fi', 'placeholder': '+91 ...'}))
    bio        = forms.CharField(required=False,  widget=forms.Textarea(attrs={'class': 'fi', 'rows': 2, 'placeholder': 'Short bio...'}))

    def clean_username(self):
        uname = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=uname).exists():
            raise forms.ValidationError("Username already taken.")
        return uname

    def save(self):
        import random
        d = self.cleaned_data
        user = User.objects.create_user(
            username=d['username'], password=d['password'],
            first_name=d['first_name'], last_name=d.get('last_name', ''),
            email=d.get('email', ''),
        )
        colors = ['#6366f1','#8b5cf6','#ec4899','#14b8a6','#f59e0b','#10b981','#3b82f6','#f43f5e']
        Profile.objects.create(
            user=user, role='mentee',
            subject=d.get('subject',''), phone=d.get('phone',''),
            bio=d.get('bio',''), avatar_color=random.choice(colors),
        )
        return user


class MenteeEditForm(forms.Form):
    first_name = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class': 'fi'}))
    last_name  = forms.CharField(max_length=50,  required=False, widget=forms.TextInput(attrs={'class': 'fi'}))
    email      = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'fi'}))
    subject    = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'fi'}))
    phone      = forms.CharField(max_length=20,  required=False, widget=forms.TextInput(attrs={'class': 'fi'}))
    bio        = forms.CharField(required=False,  widget=forms.Textarea(attrs={'class': 'fi', 'rows': 2}))


class MeetingForm(forms.ModelForm):
    meeting_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'fi'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model  = Meeting
        fields = ['title', 'description', 'meeting_date']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'fi', 'placeholder': 'e.g. Weekly Check-in'}),
            'description': forms.Textarea(attrs={'class': 'fi', 'rows': 3, 'placeholder': 'Agenda / what to discuss...'}),
        }


class MeetingNotesForm(forms.ModelForm):
    class Meta:
        model  = Meeting
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'fi', 'rows': 4, 'placeholder': 'Post-meeting notes, action items...'})
        }
