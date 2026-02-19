from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import safe_join
import os
from datetime import datetime

from config import Config
from utils.auth import login_required, verify_password
from utils.security import add_security_headers
from utils.pdf_generator import generate_verification_report

app = Flask(__name__)
app.config.from_object(Config)

limiter = Limiter(app=app, key_func=get_remote_address)

# 🔐 SECURITY HEADERS
@app.after_request
def apply_security_headers(response):
    return add_security_headers(response)

# ============================
# ROUTES
# ============================

@app.route('/')
def index():
    return render_template('index.html')

# ---------- AUTH ----------
@app.route('/api/verify-password', methods=['POST'])
@limiter.limit("100 per hour")
def verify_password_route():
    data = request.get_json()
    password = data.get('password', '')

    if not password:
        return jsonify({'error': 'Password required'}), 400

    current_password = os.getenv('ACCESS_PASSWORD', Config.ACCESS_PASSWORD)

    if verify_password(password, current_password):
        session.clear()
        session['authenticated'] = True
        session['authenticated_at'] = datetime.utcnow().isoformat()

        return jsonify({'success': True})

    return jsonify({'error': 'Invalid password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ---------- STATUS ----------
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'authenticated': bool(session.get('authenticated')),
        'password_changed': app.config.get('PASSWORD_CHANGED', False)
    })

@app.route('/api/acknowledge-password-change', methods=['POST'])
def acknowledge_password_change():
    app.config['PASSWORD_CHANGED'] = False
    session.clear()
    return jsonify({'success': True})

# ---------- IDENTITY ----------
@app.route('/api/identity')
@login_required
def identity():
    return jsonify({'success': True, 'data': Config.DEMO_IDENTITY})

# ---------- DOCUMENTS ----------
@app.route('/api/documents/<doc_type>')
@login_required
def documents(doc_type):
    allowed = ['aadhaar', 'pan', 'passport']
    if doc_type not in allowed:
        return jsonify({'error': 'Invalid document'}), 400

    folder = 'view'
    filename = f'{doc_type}_demo.pdf'
    path = safe_join(app.static_folder, folder, filename)

    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404

    return send_file(path, mimetype='application/pdf')

# ---------- REPORT ----------
@app.route('/api/generate-report')
@login_required
def generate_report():
    pdf = generate_verification_report(Config.DEMO_IDENTITY)
    return send_file(pdf, as_attachment=True, download_name='verification_report.pdf')

# ============================
# 🔥 WEBHOOK — PASSWORD UPDATE
# ============================
@app.route('/api/admin/update-password', methods=['POST'])
@limiter.limit("10 per minute")
def update_password():
    import hmac

    admin_secret = os.getenv('ADMIN_SECRET', '')
    auth = request.headers.get('Authorization', '')

    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401

    token = auth.replace('Bearer ', '')

    if not hmac.compare_digest(token, admin_secret):
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({'error': 'Password required'}), 400

    # 🔐 Update password
    os.environ['ACCESS_PASSWORD'] = new_password
    Config.ACCESS_PASSWORD = new_password

    # 🔥 Force logout for dashboard users
    app.config['PASSWORD_CHANGED'] = True

    return jsonify({'success': True, 'message': 'Password updated'})

# ---------- ERRORS ----------
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
