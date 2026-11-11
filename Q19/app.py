from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory store for suggestions
suggestions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    category = data.get('category', '').strip()
    message = data.get('message', '').strip()

    # Validation
    if not name:
        return jsonify({'success': False, 'error': 'Name is required.'})
    if not email or '@' not in email:
        return jsonify({'success': False, 'error': 'A valid email is required.'})
    if not message:
        return jsonify({'success': False, 'error': 'Suggestion message cannot be empty.'})

    suggestion = {
        'id': len(suggestions) + 1,
        'name': name,
        'email': email,
        'category': category if category else 'General',
        'message': message,
        'timestamp': datetime.now().strftime('%d %b %Y, %I:%M %p')
    }
    suggestions.append(suggestion)

    return jsonify({
        'success': True,
        'message': f'Thank you, {name}! Your suggestion has been submitted.',
        'total': len(suggestions)
    })

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    return jsonify({'suggestions': suggestions[::-1]})  # newest first

if __name__ == '__main__':
    app.run(debug=True)