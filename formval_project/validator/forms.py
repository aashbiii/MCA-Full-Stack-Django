import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Registration


# ── Custom field-level validators ─────────────────────────────────────────────

def validate_no_numbers(value):
    """Name must not contain digits."""
    if any(char.isdigit() for char in value):
        raise ValidationError("Name must not contain numbers.")

def validate_username(value):
    """Username: 4–30 chars, alphanumeric + underscores only."""
    if len(value) < 4:
        raise ValidationError("Username must be at least 4 characters long.")
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError("Username may only contain letters, numbers, and underscores.")

def validate_phone(value):
    """Phone: digits, spaces, +, -, () allowed."""
    cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
    if not cleaned.isdigit():
        raise ValidationError("Enter a valid phone number (digits, spaces, +, -, () allowed).")
    if not (7 <= len(cleaned) <= 15):
        raise ValidationError("Phone number must be between 7 and 15 digits.")


# ── Registration Form ──────────────────────────────────────────────────────────

class RegistrationForm(forms.ModelForm):

    # Extra field (not in model) for password confirmation
    password  = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'class': 'fi'}),
        min_length=8,
        help_text="Minimum 8 characters, at least one digit.",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'fi'}),
        label="Confirm Password",
    )

    class Meta:
        model  = Registration
        fields = ['first_name', 'last_name', 'username', 'email',
                  'phone', 'age', 'website', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John',      'class': 'fi'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Doe',       'class': 'fi'}),
            'username':   forms.TextInput(attrs={'placeholder': 'john_doe',  'class': 'fi'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'john@example.com', 'class': 'fi'}),
            'phone':      forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'class': 'fi'}),
            'age':        forms.NumberInput(attrs={'placeholder': '18', 'class': 'fi'}),
            'website':    forms.URLInput(attrs={'placeholder': 'https://yoursite.com', 'class': 'fi'}),
            'bio':        forms.Textarea(attrs={'placeholder': 'Tell us about yourself...', 'rows': 3, 'class': 'fi'}),
        }

    # ── Field-level clean methods ──────────────────────────────────────────────

    def clean_first_name(self):
        value = self.cleaned_data['first_name'].strip()
        validate_no_numbers(value)
        if len(value) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        return value.title()

    def clean_last_name(self):
        value = self.cleaned_data['last_name'].strip()
        validate_no_numbers(value)
        if len(value) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        return value.title()

    def clean_username(self):
        value = self.cleaned_data['username'].strip().lower()
        validate_username(value)
        if Registration.objects.filter(username__iexact=value).exists():
            raise ValidationError("This username is already taken.")
        return value

    def clean_email(self):
        value = self.cleaned_data['email'].strip().lower()
        if Registration.objects.filter(email__iexact=value).exists():
            raise ValidationError("An account with this email already exists.")
        return value

    def clean_phone(self):
        value = self.cleaned_data['phone'].strip()
        validate_phone(value)
        return value

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 13:
            raise ValidationError("You must be at least 13 years old to register.")
        if age > 120:
            raise ValidationError("Please enter a valid age.")
        return age

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if password.islower():
            raise ValidationError("Password must contain at least one uppercase letter.")
        return password

    # ── Cross-field (form-level) clean ─────────────────────────────────────────

    def clean(self):
        cleaned_data = super().clean()
        password  = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")

        # Cross-field: username must not contain first name
        username   = cleaned_data.get('username', '')
        first_name = cleaned_data.get('first_name', '').lower()
        if first_name and first_name in username:
            self.add_error('username', "Username should not contain your first name.")

        return cleaned_data
