from django.shortcuts import render, redirect

# Home — shows session info
def home(request):
    visit_count = request.session.get('visit_count', 0) + 1
    request.session['visit_count'] = visit_count

    username = request.session.get('username', None)
    theme    = request.session.get('theme', 'light')
    messages = request.session.get('messages', [])

    return render(request, 'home.html', {
        'visit_count': visit_count,
        'username':    username,
        'theme':       theme,
        'messages':    messages,
        'session_key': request.session.session_key,
    })

# Login — store username in session
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password == 'pass123':
            request.session['username'] = username
            request.session['messages'] = request.session.get('messages', [])
            return redirect('home')
        else:
            error = 'Invalid credentials. Use any username with password: pass123'
    return render(request, 'login.html', {'error': error})

# Logout — clear session
def logout_view(request):
    request.session.flush()
    return redirect('home')

# Set theme preference in session
def set_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        request.session['theme'] = theme
    return redirect('home')

# Add a message to session
def add_message(request):
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            msgs = request.session.get('messages', [])
            msgs.append(msg)
            request.session['messages'] = msgs
            request.session.modified = True
    return redirect('home')

# Clear messages from session
def clear_messages(request):
    request.session['messages'] = []
    request.session.modified = True
    return redirect('home')

# Set session expiry
def set_expiry(request):
    if request.method == 'POST':
        expiry = int(request.POST.get('expiry', 0))
        request.session.set_expiry(expiry)
    return redirect('home')
