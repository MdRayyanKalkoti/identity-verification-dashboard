# ============================================
# COMPLETE app.py FILE
# ============================================
# Replace your entire app.py with this file
# Only change: generate_report route now includes ID numbers

from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
from config import Config
from utils.auth import login_required
from utils.security import validate_password
from utils.pdf_generator import generate_verification_report
import os
import json

# ============================================
# APP INITIALIZATION
# ============================================
app = Flask(__name__)
app.config.from_object(Config)

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ============================================
# HELPER FUNCTIONS FOR PASSWORD SYNC
# ============================================
def get_password_file_path():
    """Get path to password storage file"""
    return os.path.join(os.path.dirname(__file__), '.password_sync')

def save_password_to_file(password):
    """Save password to persistent file"""
    try:
        password_file = get_password_file_path()
        with open(password_file, 'w') as f:
            json.dump({'password': password, 'updated_at': datetime.now().isoformat()}, f)
        print(f"✅ Password saved to file: {password_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving password: {e}")
        return False

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Handle login authentication"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        # Get the current access password
        access_password = Config.get_access_password()
        
        if not access_password:
            return jsonify({'error': 'Server configuration error'}), 500
        
        # Validate password
        if validate_password(password, access_password):
            session['authenticated'] = True
            session['login_time'] = datetime.now().isoformat()
            session.permanent = True
            
            return jsonify({
                'success': True,
                'message': 'Login successful'
            }), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if session.get('authenticated'):
        return jsonify({
            'authenticated': True,
            'login_time': session.get('login_time')
        }), 200
    else:
        return jsonify({'authenticated': False}), 200

@app.route('/api/identity', methods=['GET'])
@login_required
def get_identity():
    """Get user identity information"""
    return jsonify(Config.DEMO_IDENTITY), 200

@app.route('/api/documents', methods=['GET'])
@login_required
def get_documents():
    """Get list of all verified documents"""
    documents = [
        # Government IDs
        {'name': 'Aadhaar Card', 'type': 'Aadhar_Card', 'category': 'Government ID', 'verified': True},
        {'name': 'PAN Card', 'type': 'Pan_Card', 'category': 'Government ID', 'verified': True},
        {'name': 'Passport', 'type': 'Passport', 'category': 'Government ID', 'verified': True},
        
        # Driving Documents
        {'name': 'Driving License', 'type': 'Driving_Licence', 'category': 'Driving Document', 'verified': True},
        {'name': 'International Driving Permit', 'type': 'idp', 'category': 'Driving Document', 'verified': True},
        {'name': 'Medical Certificate (Form 1A)', 'type': 'Medical_Certificate_Form1A', 'category': 'Driving Document', 'verified': True},
        
        # Educational
        {'name': 'BE Degree (CSE - AI & ML)', 'type': 'BE_CSE_AI_ML__Certificate', 'category': 'Educational', 'verified': True},
        {'name': 'Diploma Certificate', 'type': 'diploma_provisional_certificate', 'category': 'Educational', 'verified': True},
        
        # Professional
        {'name': 'Professional Resume', 'type': 'Mohammad_Rayyan_Kalkoti_Resume', 'category': 'Professional', 'verified': True},
        {'name': 'Bank Statement', 'type': 'Bank_Proof', 'category': 'Professional', 'verified': True},
        
        # Personal
        {'name': 'Professional Photo', 'type': 'photo', 'category': 'Personal', 'verified': True}
    ]
    
    return jsonify(documents), 200

@app.route('/api/generate-report')
@login_required
def generate_report():
    """Generate comprehensive verification report with all 11 documents and ID numbers"""
    
    # All 11 documents with their categories AND ID numbers
    documents = [
        # Government IDs
        {
            'name': 'Aadhaar Card', 
            'type': 'Aadhar_Card', 
            'category': 'Government ID', 
            'id_number': '4335 6189 7894',
            'verified': True
        },
        {
            'name': 'PAN Card', 
            'type': 'Pan_Card', 
            'category': 'Government ID', 
            'id_number': 'JKIPK0102E',
            'verified': True
        },
        {
            'name': 'Passport', 
            'type': 'Passport', 
            'category': 'Government ID', 
            'id_number': 'Y2156864',
            'verified': True
        },
        
        # Driving Documents
        {
            'name': 'Driving License', 
            'type': 'Driving_Licence', 
            'category': 'Driving Document', 
            'id_number': 'KA25 20210009210',
            'verified': True
        },
        {
            'name': 'International Driving Permit', 
            'type': 'idp', 
            'category': 'Driving Document', 
            'id_number': '46/2026/IND/KA25',
            'verified': True
        },
        {
            'name': 'Medical Certificate (Form 1A)', 
            'type': 'Medical_Certificate_Form1A', 
            'category': 'Driving Document', 
            'id_number': 'KMC No: 41523',
            'verified': True
        },
        
        # Educational
        {
            'name': 'BE Degree (CSE - AI & ML)', 
            'type': 'BE_CSE_AI_ML__Certificate', 
            'category': 'Educational', 
            'id_number': 'CGPA: 7.24/10',
            'verified': True
        },
        {
            'name': 'Diploma Certificate', 
            'type': 'diploma_provisional_certificate', 
            'category': 'Educational', 
            'id_number': 'First Class with Distinction',
            'verified': True
        },
        
        # Professional
        {
            'name': 'Professional Resume', 
            'type': 'Mohammad_Rayyan_Kalkoti_Resume', 
            'category': 'Professional', 
            'id_number': 'Backend & AI Engineer',
            'verified': True
        },
        {
            'name': 'Bank Statement', 
            'type': 'Bank_Proof', 
            'category': 'Professional', 
            'id_number': 'SBI Account - Verified',
            'verified': True
        },
        
        # Personal
        {
            'name': 'Professional Photo', 
            'type': 'photo', 
            'category': 'Personal', 
            'id_number': 'Passport Size Photo',
            'verified': True
        }
    ]
    
    # Generate PDF with all documents and ID numbers
    pdf = generate_verification_report(Config.DEMO_IDENTITY, documents)
    
    return send_file(
        pdf, 
        as_attachment=True, 
        download_name='verification_report_complete.pdf',
        mimetype='application/pdf'
    )

@app.route('/api/webhook/password-changed', methods=['POST'])
def webhook_password_changed():
    """Webhook endpoint for password change notifications from control panel"""
    try:
        data = request.get_json()
        
        # Verify admin secret
        provided_secret = data.get('admin_secret')
        expected_secret = os.getenv('ADMIN_SECRET')
        
        if not expected_secret:
            print("❌ ADMIN_SECRET not configured!")
            return jsonify({'error': 'Server configuration error'}), 500
        
        if provided_secret != expected_secret:
            print("❌ Invalid admin secret in webhook")
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get new password from webhook
        new_password = data.get('new_password')
        
        if not new_password:
            print("❌ No password in webhook payload")
            return jsonify({'error': 'Missing password'}), 400
        
        print(f"📥 Webhook received: Password update from control panel")
        
        # CRITICAL: Save password to persistent file
        if save_password_to_file(new_password):
            print(f"✅ Password synced and saved persistently")
            
            # Set flag to logout all users
            session['should_logout'] = True
            
            return jsonify({
                'status': 'success',
                'message': 'Password synced and saved',
                'action': 'all_users_will_logout'
            }), 200
        else:
            print("❌ Failed to save password to file")
            return jsonify({'error': 'Failed to save password'}), 500
            
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5000)