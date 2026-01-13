from flask import Flask, request, jsonify, send_from_directory
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(APP_DIR, 'high_scores.json')

app = Flask(__name__, static_folder=APP_DIR)

def read_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_scores(scores):
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    # serve the game page
    return send_from_directory(APP_DIR, 'game.html')

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or 'Anon')[:32]
    try:
        score = int(data.get('score', 0))
    except Exception:
        score = 0

    scores = read_scores()
    scores.append({'name': name, 'score': score})
    # keep sorted descending
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    # keep top 50
    scores = scores[:50]
    write_scores(scores)
    return jsonify({'status':'ok'})

@app.route('/scores')
def scores():
    return jsonify(read_scores())

if __name__ == '__main__':
    # simple dev server
    app.run(host='0.0.0.0', port=8000, debug=True)
