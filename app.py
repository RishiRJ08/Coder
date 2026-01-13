#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort
import os
import time
import jwt
import hmac
import hashlib
import json
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "GitHub App scaffold running"})


@app.route('/jwt')
def get_jwt():
    app_id = os.environ.get('GITHUB_APP_ID') or os.environ.get('APP_ID')
    key_path = os.environ.get('GITHUB_PRIVATE_KEY_PATH', 'secrets/app-private-key.pem')
    if not app_id:
        return jsonify({"error": "GITHUB_APP_ID not set"}), 400
    if not os.path.exists(key_path):
        return jsonify({"error": "private key not found", "path": key_path}), 400
    with open(key_path, 'rb') as f:
        private_key = f.read()
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + (9 * 60), "iss": int(app_id)}
    token = jwt.encode(payload, private_key, algorithm='RS256')
    if isinstance(token, bytes):
        token = token.decode()
    return jsonify({"jwt": token})


@app.route('/webhook', methods=['POST'])
def webhook():
    secret = os.environ.get('WEBHOOK_SECRET')
    if secret:
        signature = request.headers.get('X-Hub-Signature-256', '')
        mac = hmac.new(secret.encode(), msg=request.data, digestmod=hashlib.sha256)
        expected = 'sha256=' + mac.hexdigest()
        if not hmac.compare_digest(expected, signature):
            abort(401, "Invalid signature")
    evt = request.headers.get('X-GitHub-Event', 'unknown')
    payload = request.get_json(silent=True)
    print(f"Received event {evt}: {payload}")
    return '', 204


# Simple leaderboard endpoints used by the static `docs/index.html` game.
SCORES_PATH = Path('high_scores.json')


def load_scores():
    if not SCORES_PATH.exists():
        return []
    try:
        with SCORES_PATH.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_scores(scores):
    try:
        with SCORES_PATH.open('w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2)
        return True
    except Exception as e:
        print('Failed to save scores:', e)
        return False


@app.route('/scores', methods=['GET'])
def scores():
    scores = load_scores()
    # sort descending
    scores_sorted = sorted(scores, key=lambda s: s.get('score', 0), reverse=True)
    return jsonify(scores_sorted)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'score' not in data:
        return jsonify({'error': 'invalid payload'}), 400
    name = str(data.get('name', 'Anon'))[:64]
    try:
        score_val = int(data.get('score', 0))
    except Exception:
        score_val = 0

    scores = load_scores()
    scores.append({'name': name, 'score': score_val})
    # keep only top 100
    scores = sorted(scores, key=lambda s: s.get('score', 0), reverse=True)[:100]
    ok = save_scores(scores)
    if not ok:
        return jsonify({'error': 'failed to save'}), 500
    return jsonify({'ok': True}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
