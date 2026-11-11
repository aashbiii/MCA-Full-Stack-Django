import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request, jsonify, session
from ai_helpers_ashbi import get_response, summarize_text

app = Flask(__name__)
app.secret_key = 'ai-helpers-ashbi-flask-secret-2026'
MAX_HISTORY = 10

@app.route('/')
def index():
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', history=session['history'])

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data   = request.get_json()
        prompt = data.get('prompt', '').strip()
        action = data.get('action', 'respond')

        if not prompt:
            return jsonify({'error': 'Please enter a prompt.'}), 400

        if action == 'summarize':
            result = {
                'prompt':     prompt,
                'response':   summarize_text(prompt, max_sentences=2),
                'category':   'summary',
                'word_count': len(summarize_text(prompt).split()),
            }
        else:
            result = get_response(prompt)

        history = session.get('history', [])
        history.insert(0, {
            'prompt':     result['prompt'][:80] + ('...' if len(result['prompt']) > 80 else ''),
            'category':   result['category'],
            'word_count': result['word_count'],
        })
        session['history']  = history[:MAX_HISTORY]
        session.modified    = True

        return jsonify({
            'response':   result['response'],
            'category':   result['category'],
            'word_count': result['word_count'],
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['history'] = []
    session.modified = True
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
