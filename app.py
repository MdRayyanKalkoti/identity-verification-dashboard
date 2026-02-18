from dotenv import load_dotenv
load_dotenv()  # MUST BE FIRST - Load environment variables

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

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply security headers to all responses
@app.after_request
def apply_security_headers(response):
    return add_security_headers(response)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Serve main application page"""
    return render_template('index.html')

@app.route('/api/verify-password', methods=['POST'])
@limiter.limit("100 per hour")  # Increased for testing
def verify_password_route():
    """Verify access password and create session"""
    data = request.get_json()
    provided_password = data.get('password', '')
    
    if not provided_password:
        return jsonify({'error': 'Password required'}), 400
    
    if verify_password(provided_password, Config.get_access_password()):
        session['authenticated'] = True
        session['authenticated_at'] = datetime.now().isoformat()
        return jsonify({
            'success': True,
            'message': 'Access granted'
        })
    else:
        return jsonify({
            'error': 'Invalid password',
            'locked': True
        }), 401

@app.route('/api/identity', methods=['GET'])
@login_required
def get_identity():
    """Get identity information"""
    return jsonify({
        'success': True,
        'data': Config.DEMO_IDENTITY
    })

@app.route('/api/documents/<doc_type>', methods=['GET'])
@login_required
def get_document(doc_type):
    """Serve document PDF - separate folders for view vs download"""
    allowed_docs = ['aadhaar', 'pan', 'passport']
    
    if doc_type not in allowed_docs:
        return jsonify({'error': 'Invalid document type'}), 400
    
    action = request.args.get('action', 'view')
    filename = f"{doc_type}_demo.pdf"
    
    # Different folders based on action
    if action == 'download':
        # Use documents folder for downloads (high quality)
        folder = 'documents'
    else:
        # Use view folder for viewing (optimized for web)
        folder = 'view'
    
    filepath = safe_join(app.static_folder, folder, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': f'Document not found in {folder} folder'}), 404
    
    if action == 'download':
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    else:
        # For viewing - send inline
        return send_file(
            filepath,
            mimetype='application/pdf'
        )

@app.route('/api/generate-report', methods=['GET'])
@login_required
def generate_report():
    """Generate comprehensive verification report"""
    try:
        pdf_buffer = generate_verification_report(Config.DEMO_IDENTITY)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='verification_report.pdf'
        )
    except Exception as e:
        app.logger.error(f"Report generation failed: {str(e)}")
        return jsonify({'error': 'Report generation failed'}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Check authentication status"""
    return jsonify({
        'authenticated': session.get('authenticated', False),
        'locked': not session.get('authenticated', False)
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Clear session and logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})

# Development route to show password
@app.route('/api/dev/password', methods=['GET'])
def show_password():
    """Development only - show access password"""
    if app.config['DEBUG']:
        return jsonify({
            'password': Config.get_access_password(),
            'warning': 'This endpoint is for development only'
        })
    return jsonify({'error': 'Not available'}), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('static/documents', exist_ok=True)
    os.makedirs('static/view', exist_ok=True)
    
    # Print password for development
    print("\n" + "="*60)
    print("🔐 VERIFICATION DASHBOARD SERVER")
    print("="*60)
    print(f"Access Password: {Config.get_access_password()}")
    print(f"Password from .env: {os.getenv('ACCESS_PASSWORD')}")
    print("="*60)
    print("\n📁 PDF Folders:")
    print("   • static/view/      - For viewing in modal")
    print("   • static/documents/ - For downloading")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)