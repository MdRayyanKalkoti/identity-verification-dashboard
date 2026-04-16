# ============================================================================
# VERIFICATION DASHBOARD - SECURE CONFIGURATION
# ============================================================================
# This config.py is SAFE to upload to GitHub
# All sensitive ID numbers are loaded from environment variables
# File: config.py

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================
class Config:
    """Flask application configuration"""
    
    # Flask secret key for session encryption
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    
    # Debug mode (False in production)
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 31536000  # 365 days in seconds

# ============================================================================
# DEMO IDENTITY - SECURE VERSION
# ============================================================================
# ID numbers are loaded from environment variables
# This way, the actual numbers are NOT in the code
# Safe to upload to GitHub!

DEMO_IDENTITY = {
    # Personal Information
    'name': os.getenv('PERSON_NAME', 'Mohammad Rayyan Kalkoti'),
    'dob': os.getenv('PERSON_DOB', '01/01/2000'),
    'gender': os.getenv('PERSON_GENDER', 'Male'),
    'blood_group': os.getenv('PERSON_BLOOD_GROUP', 'O+'),
    'nationality': os.getenv('PERSON_NATIONALITY', 'Indian'),
    
    # Government IDs - All from environment variables
    'aadhaar': os.getenv('AADHAAR_NO', 'XXXX-XXXX-XXXX'),
    'aadhaar_no': os.getenv('AADHAAR_NO', 'XXXX-XXXX-XXXX'),  # Dual field support
    'pan': os.getenv('PAN_NO', 'XXXXXXXXXX'),
    'pan_no': os.getenv('PAN_NO', 'XXXXXXXXXX'),  # Dual field support
    'passport_no': os.getenv('PASSPORT_NO', 'XXXXXXXXX'),
    
    # Driving Related
    'dl_no': os.getenv('DL_NO', 'XXXXXXXXXXXX'),
    'idp_no': os.getenv('IDP_NO', 'XXXXXXXXX'),
    
    # Educational
    'degree_reg_no': os.getenv('DEGREE_REG_NO', 'XXXXXXXXXX'),
    'diploma_reg_no': os.getenv('DIPLOMA_REG_NO', 'XXXXXXXXXX'),
    
    # Professional
    'bank_account': os.getenv('BANK_ACCOUNT_NO', 'XXXXXXXXXXXX'),
    'ifsc': os.getenv('BANK_IFSC', 'XXXXXXXXXXX'),
    
    # Contact
    'phone': os.getenv('PERSON_PHONE', '+91-XXXXXXXXXX'),
    'email': os.getenv('PERSON_EMAIL', 'email@example.com'),
    'address': os.getenv('PERSON_ADDRESS', 'Address not set')
}

# ============================================================================
# PASSWORD MANAGEMENT
# ============================================================================

def get_access_password():
    """
    Get access password from multiple sources
    Priority: .password_sync file > .env file > default
    
    Returns:
        str: The access password
    """
    # Try to read from password sync file (set by control panel)
    password_sync_file = '.password_sync'
    if os.path.exists(password_sync_file):
        try:
            with open(password_sync_file, 'r') as f:
                data = json.load(f)
                if data.get('password'):
                    return data['password']
        except Exception as e:
            print(f"Warning: Could not read .password_sync file: {e}")
    
    # Fallback to environment variable
    return os.getenv('ACCESS_PASSWORD', 'changeme123')

# Get admin secret for webhook authentication
ADMIN_SECRET = os.getenv('ADMIN_SECRET', 'change-this-admin-secret')

# ============================================================================
# DOCUMENT CONFIGURATION
# ============================================================================
# You can optionally use cloud storage URLs instead of local files
# Set DOCUMENT_BASE_URL in environment to use cloud storage

DOCUMENT_BASE_URL = os.getenv('DOCUMENT_BASE_URL', '')

if DOCUMENT_BASE_URL:
    # Using cloud storage (S3, Google Cloud, etc.)
    DOCUMENT_PATHS = {
        'aadhar': f"{DOCUMENT_BASE_URL}/Aadhar_Card.pdf",
        'pan': f"{DOCUMENT_BASE_URL}/Pan_Card.pdf",
        'passport': f"{DOCUMENT_BASE_URL}/Passport.pdf",
        'dl': f"{DOCUMENT_BASE_URL}/Driving_Licence.pdf",
        'idp': f"{DOCUMENT_BASE_URL}/idp.pdf",
        'medical': f"{DOCUMENT_BASE_URL}/Medical_Certificate_Form1A.pdf",
        'degree': f"{DOCUMENT_BASE_URL}/BE_CSE_AI_ML__Certificate.pdf",
        'diploma': f"{DOCUMENT_BASE_URL}/diploma_provisional_certificate.pdf",
        'resume': f"{DOCUMENT_BASE_URL}/Mohammad_Rayyan_Kalkoti_Resume.pdf",
        'bank': f"{DOCUMENT_BASE_URL}/Bank_Proof.pdf",
        'photo': f"{DOCUMENT_BASE_URL}/photo.pdf"
    }
else:
    # Using local files
    DOCUMENT_PATHS = {
        'aadhar': 'static/documents/Aadhar_Card.pdf',
        'pan': 'static/documents/Pan_Card.pdf',
        'passport': 'static/documents/Passport.pdf',
        'dl': 'static/documents/Driving_Licence.pdf',
        'idp': 'static/documents/idp.pdf',
        'medical': 'static/documents/Medical_Certificate_Form1A.pdf',
        'degree': 'static/documents/BE_CSE_AI_ML__Certificate.pdf',
        'diploma': 'static/documents/diploma_provisional_certificate.pdf',
        'resume': 'static/documents/Mohammad_Rayyan_Kalkoti_Resume.pdf',
        'bank': 'static/documents/Bank_Proof.pdf',
        'photo': 'static/documents/photo.pdf'
    }

# ============================================================================
# INSTRUCTIONS FOR DEPLOYMENT
# ============================================================================
"""
GITHUB DEPLOYMENT:
------------------
This config.py is SAFE to upload to GitHub because:
✅ No real ID numbers (all from environment variables)
✅ No real passwords (all from environment variables)
✅ No sensitive data hardcoded

RENDER DEPLOYMENT:
------------------
Set these environment variables in Render dashboard:

Required:
- ACCESS_PASSWORD=your_secure_password
- SECRET_KEY=<generate-with-python-secrets>
- ADMIN_SECRET=<same-as-control-panel>

Your ID Numbers:
- AADHAAR_NO=your_aadhaar_number
- PAN_NO=your_pan_number
- PASSPORT_NO=your_passport_number
- DL_NO=your_dl_number
- IDP_NO=your_idp_number
- DEGREE_REG_NO=your_degree_reg_number
- DIPLOMA_REG_NO=your_diploma_reg_number
- BANK_ACCOUNT_NO=your_bank_account
- BANK_IFSC=your_ifsc_code

Personal Info (optional):
- PERSON_NAME=Your Name
- PERSON_DOB=DD/MM/YYYY
- PERSON_PHONE=+91-XXXXXXXXXX
- PERSON_EMAIL=your@email.com

Optional:
- FLASK_DEBUG=False
- DOCUMENT_BASE_URL=https://your-cloud-storage.com/documents

GENERATE SECRETS:
-----------------
SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"

ADMIN_SECRET:
python -c "import secrets; print(secrets.token_urlsafe(32))"
"""
