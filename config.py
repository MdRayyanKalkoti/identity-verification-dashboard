# ============================================
# COMPLETE config.py FILE
# ============================================
# Replace your entire config.py with this

import os
import json
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Admin configuration
    ADMIN_SECRET = os.getenv('ADMIN_SECRET', 'change-this-admin-secret')
    
    @staticmethod
    def get_access_password():
        """
        Get access password with priority:
        1. From persistent file (synced from control panel)
        2. From environment variable (fallback)
        """
        # First, try to load from persistent file
        try:
            password_file = os.path.join(os.path.dirname(__file__), '.password_sync')
            if os.path.exists(password_file):
                with open(password_file, 'r') as f:
                    data = json.load(f)
                    password = data.get('password')
                    if password:
                        print(f"✅ Using password from control panel sync (updated: {data.get('updated_at')})")
                        return password
        except Exception as e:
            print(f"⚠️ Could not read synced password: {e}")
        
        # Fallback to environment variable
        password = os.getenv('ACCESS_PASSWORD', '')
        if password:
            print("ℹ️ Using password from environment variable")
        else:
            print("⚠️ No password found in sync file or environment!")
        
        return password
    
    # Demo identity information
    DEMO_IDENTITY = {
        # Basic Information
        'name': 'Mohammad Rayyan Kalkoti',
        'dob': 'December 24, 2001',
        'nationality': 'Indian',
        'address': 'Rasheed Shama Manzil, L S Tank Road, Near Rayarmatha, Hubballi-Dharwad, Karnataka 580007, India',
        
        # Government IDs - Both field name formats for compatibility
        'aadhaar': '4335 6189 7894',
        'pan': 'JKIPK0102E',
        'passport': 'Y2156864',
        'aadhaar_no': '4335 6189 7894',
        'pan_no': 'JKIPK0102E',
        'passport_no': 'Y2156864',
        
        # Driving Documents
        'dl_no': 'KA25 20210009210',
        'idp_no': '46/2026/IND/KA25',
        'medical_cert_no': 'KMC No: 41523',
        
        # Educational
        'education': 'B.Tech - Computer Science (AI & ML)',
        'institution': 'M.S. Ramaiah Institute of Technology, Bangalore',
        'grade': 'First Class with Distinction',
        'cgpa': '7.24 / 10',
        
        # Professional
        'profession': 'Backend & AI Engineer',
        'availability': 'Immediate Joining',
        'preferred_location': 'Federal Territory of Kuala Lumpur, Malaysia',
        
        # Banking
        'bank_account': 'SBI Account (Verified)',
        
        # Contact
        'email': 'rayyanaiengineer@gmail.com',
        'phone': '+91 90196 04204'
    }