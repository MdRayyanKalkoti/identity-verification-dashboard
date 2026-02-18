import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)
    ACCESS_PASSWORD = os.getenv('ACCESS_PASSWORD') or secrets.token_urlsafe(16)
    
    # Session - FIXED: Use null session to avoid Flask-Session bugs
    SESSION_TYPE = 'null'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Security Headers
    SEND_FILE_MAX_AGE_DEFAULT = 0
    
    # Application
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Demo Data
    DEMO_IDENTITY = {
        'name': 'Mohammad Rayyan Kalkoti',
        'aadhaar': '361691616165',
        'pan': 'XXXPX1234X',
        'passport': '516161156',
        'dob': '24/12/2001',
        'verification_status': 'VERIFIED',
        'verification_date': '2026-02-16'
    }
    
    @staticmethod
    def get_access_password():
        """Get the current access password"""
        return Config.ACCESS_PASSWORD