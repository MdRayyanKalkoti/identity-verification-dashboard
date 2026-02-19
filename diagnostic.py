#!/usr/bin/env python3
"""
DIAGNOSTIC SCRIPT FOR RAYYAN-ID (VERIFICATION DASHBOARD)
Run this to check if everything is configured correctly
"""

import os
import sys
from datetime import datetime

print("="*70)
print("🔍 RAYYAN-ID VERIFICATION DASHBOARD - DIAGNOSTIC REPORT")
print("="*70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# Track issues
issues = []
warnings = []

# ============================================================================
# 1. PYTHON VERSION CHECK
# ============================================================================
print("\n📌 1. PYTHON VERSION")
print("-" * 70)
print(f"Python Version: {sys.version}")
python_version = sys.version_info
if python_version.major == 3 and python_version.minor >= 8:
    print("✅ Python version OK (3.8+)")
else:
    issues.append("❌ Python version should be 3.8 or higher")
    print("❌ Python version should be 3.8 or higher")

# ============================================================================
# 2. ENVIRONMENT VARIABLES CHECK
# ============================================================================
print("\n📌 2. ENVIRONMENT VARIABLES")
print("-" * 70)

# Check ACCESS_PASSWORD
access_password = os.getenv('ACCESS_PASSWORD')
if access_password:
    print(f"✅ ACCESS_PASSWORD: Set (length: {len(access_password)} chars)")
    if len(access_password) < 6:
        warnings.append("⚠️ ACCESS_PASSWORD is very short (< 6 characters)")
        print("⚠️ Warning: Password is very short (< 6 characters)")
    # Show partial password for verification
    masked = access_password[:3] + "*" * (len(access_password) - 6) + access_password[-3:] if len(access_password) > 6 else "***"
    print(f"   Preview: {masked}")
else:
    issues.append("❌ ACCESS_PASSWORD not set!")
    print("❌ ACCESS_PASSWORD: NOT SET!")

# Check SECRET_KEY
secret_key = os.getenv('SECRET_KEY')
if secret_key:
    print(f"✅ SECRET_KEY: Set (length: {len(secret_key)} chars)")
    if len(secret_key) < 32:
        warnings.append("⚠️ SECRET_KEY is short (< 32 characters)")
        print("⚠️ Warning: SECRET_KEY is short (< 32 characters)")
else:
    warnings.append("⚠️ SECRET_KEY not set (will auto-generate)")
    print("⚠️ SECRET_KEY: Not set (will auto-generate)")

# Check FLASK_DEBUG
flask_debug = os.getenv('FLASK_DEBUG', 'False')
print(f"✅ FLASK_DEBUG: {flask_debug}")
if flask_debug.lower() == 'true':
    warnings.append("⚠️ FLASK_DEBUG is True (should be False in production)")
    print("⚠️ Warning: FLASK_DEBUG should be False in production")

# ============================================================================
# 3. IMPORT CHECKS
# ============================================================================
print("\n📌 3. REQUIRED MODULES")
print("-" * 70)

required_modules = [
    'flask',
    'flask_limiter',
    'werkzeug',
    'dotenv',
    'reportlab'
]

for module_name in required_modules:
    try:
        if module_name == 'dotenv':
            __import__('dotenv')
            module = sys.modules['dotenv']
        else:
            module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {module_name}: {version}")
    except ImportError:
        issues.append(f"❌ Missing module: {module_name}")
        print(f"❌ {module_name}: NOT INSTALLED")

# ============================================================================
# 4. FILE STRUCTURE CHECK
# ============================================================================
print("\n📌 4. FILE STRUCTURE")
print("-" * 70)

required_files = {
    'app.py': 'Main application file',
    'config.py': 'Configuration file',
    'utils/auth.py': 'Authentication module',
    'utils/security.py': 'Security module',
    'utils/pdf_generator.py': 'PDF generator',
    'templates/index.html': 'Main HTML template',
    'static/css/style.css': 'Stylesheet',
    'static/js/app.js': 'JavaScript file'
}

for file_path, description in required_files.items():
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {file_path}: {size:,} bytes - {description}")
    else:
        issues.append(f"❌ Missing: {file_path}")
        print(f"❌ {file_path}: MISSING - {description}")

# Check PDF files
pdf_dirs = ['static/view', 'static/documents']
print("\n   PDF Files:")
for pdf_dir in pdf_dirs:
    if os.path.exists(pdf_dir):
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        if pdf_files:
            print(f"   ✅ {pdf_dir}: {len(pdf_files)} PDF files")
            for pdf in pdf_files:
                print(f"      - {pdf}")
        else:
            warnings.append(f"⚠️ No PDF files in {pdf_dir}")
            print(f"   ⚠️ {pdf_dir}: No PDF files")
    else:
        warnings.append(f"⚠️ Directory missing: {pdf_dir}")
        print(f"   ⚠️ {pdf_dir}: Directory missing")

# ============================================================================
# 5. CONFIGURATION TEST
# ============================================================================
print("\n📌 5. CONFIGURATION LOADING")
print("-" * 70)

try:
    from config import Config
    print("✅ Config module imported successfully")
    
    # Test password retrieval
    password = Config.get_access_password()
    if password:
        masked = password[:3] + "*" * (len(password) - 6) + password[-3:] if len(password) > 6 else "***"
        print(f"✅ ACCESS_PASSWORD loaded: {masked}")
    else:
        issues.append("❌ Config.get_access_password() returned empty")
        print("❌ get_access_password() returned empty")
    
    # Check demo identity
    if hasattr(Config, 'DEMO_IDENTITY'):
        print(f"✅ DEMO_IDENTITY configured: {Config.DEMO_IDENTITY.get('name', 'Unknown')}")
    
except Exception as e:
    issues.append(f"❌ Error loading config: {str(e)}")
    print(f"❌ Error loading config: {str(e)}")

# ============================================================================
# 6. AUTHENTICATION TEST
# ============================================================================
print("\n📌 6. AUTHENTICATION SYSTEM")
print("-" * 70)

try:
    from utils.auth import verify_password, login_required
    print("✅ Auth module imported successfully")
    
    # Test password verification
    test_password = "test123"
    result = verify_password(test_password, test_password)
    if result:
        print("✅ Password verification function works (identical passwords)")
    else:
        issues.append("❌ Password verification failed for identical passwords")
        print("❌ Password verification failed for identical passwords")
    
    # Test with different passwords
    result = verify_password("test123", "wrong456")
    if not result:
        print("✅ Password verification correctly rejects wrong passwords")
    else:
        issues.append("❌ Password verification accepts wrong passwords!")
        print("❌ Password verification accepts wrong passwords!")
        
except Exception as e:
    issues.append(f"❌ Error testing auth: {str(e)}")
    print(f"❌ Error testing auth: {str(e)}")

# ============================================================================
# 7. SECURITY HEADERS TEST
# ============================================================================
print("\n📌 7. SECURITY MODULE")
print("-" * 70)

try:
    from utils.security import add_security_headers
    print("✅ Security module imported successfully")
    print("✅ Security headers function available")
except Exception as e:
    issues.append(f"❌ Error loading security: {str(e)}")
    print(f"❌ Error loading security: {str(e)}")

# ============================================================================
# 8. PDF GENERATOR TEST
# ============================================================================
print("\n📌 8. PDF GENERATOR")
print("-" * 70)

try:
    from utils.pdf_generator import generate_verification_report
    print("✅ PDF generator imported successfully")
    
    # Try generating a test report
    try:
        from config import Config
        test_pdf = generate_verification_report(Config.DEMO_IDENTITY)
        if test_pdf:
            print(f"✅ Test PDF generated successfully ({len(test_pdf)} bytes)")
        else:
            warnings.append("⚠️ PDF generation returned empty")
            print("⚠️ PDF generation returned empty")
    except Exception as e:
        warnings.append(f"⚠️ PDF generation test failed: {str(e)}")
        print(f"⚠️ PDF generation test failed: {str(e)}")
        
except Exception as e:
    issues.append(f"❌ Error loading PDF generator: {str(e)}")
    print(f"❌ Error loading PDF generator: {str(e)}")

# ============================================================================
# 9. RENDER ENVIRONMENT DETECTION
# ============================================================================
print("\n📌 9. DEPLOYMENT ENVIRONMENT")
print("-" * 70)

render_detected = os.getenv('RENDER')
if render_detected:
    print("✅ Running on Render")
    render_service_name = os.getenv('RENDER_SERVICE_NAME', 'Unknown')
    print(f"   Service Name: {render_service_name}")
    render_external_url = os.getenv('RENDER_EXTERNAL_URL', 'Unknown')
    print(f"   External URL: {render_external_url}")
else:
    print("ℹ️  Running locally (not on Render)")
    print("   This is normal for development")

# ============================================================================
# 10. FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("📊 DIAGNOSTIC SUMMARY")
print("="*70)

if not issues and not warnings:
    print("✅ ALL CHECKS PASSED! System is healthy!")
else:
    if issues:
        print(f"❌ CRITICAL ISSUES FOUND: {len(issues)}")
        for issue in issues:
            print(f"   {issue}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS: {len(warnings)}")
        for warning in warnings:
            print(f"   {warning}")

# ============================================================================
# 11. RECOMMENDATIONS
# ============================================================================
print("\n" + "="*70)
print("💡 RECOMMENDATIONS")
print("="*70)

if issues:
    print("\n🔧 CRITICAL FIXES NEEDED:")
    if not access_password:
        print("   1. Set ACCESS_PASSWORD environment variable on Render")
        print("      Go to: Service → Environment → Add Variable")
        print("      Key: ACCESS_PASSWORD")
        print("      Value: Your chosen password")
    
    if any("Missing module" in issue for issue in issues):
        print("   2. Install missing Python packages:")
        print("      pip install -r requirements.txt")
    
    if any("Missing:" in issue for issue in issues):
        print("   3. Ensure all required files are present")
        print("      Check file structure matches project requirements")

if warnings:
    print("\n⚠️  SUGGESTED IMPROVEMENTS:")
    if flask_debug.lower() == 'true':
        print("   1. Set FLASK_DEBUG=False in production")
    
    if secret_key and len(secret_key) < 32:
        print("   2. Use a longer SECRET_KEY (32+ characters)")
        print("      Generate with: python -c 'import secrets; print(secrets.token_hex(32))'")
    
    if access_password and len(access_password) < 8:
        print("   3. Use a longer ACCESS_PASSWORD (8+ characters)")

print("\n" + "="*70)
print("END OF DIAGNOSTIC REPORT")
print("="*70)
print("\nℹ️  Save this report for troubleshooting")
print("ℹ️  Run this script after making changes to verify fixes")
print("="*70)