#!/usr/bin/env python3
# ============================================
# VERIFICATION DASHBOARD - COMPREHENSIVE DIAGNOSTIC
# ============================================
# Complete diagnostic with all checks
# Run: python diagnostic.py (quick check)
# Run: python diagnostic.py --full (detailed check)

import os
import sys
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================
FULL_MODE = '--full' in sys.argv or '-f' in sys.argv

# List of all 11 expected documents
EXPECTED_DOCUMENTS = [
    'Aadhar_Card.pdf',
    'Pan_Card.pdf',
    'Passport.pdf',
    'Driving_Licence.pdf',
    'idp.pdf',
    'Medical_Certificate_Form1A.pdf',
    'BE_CSE_AI_ML__Certificate.pdf',
    'diploma_provisional_certificate.pdf',
    'Mohammad_Rayyan_Kalkoti_Resume.pdf',
    'Bank_Proof.pdf',
    'photo.pdf'
]

# Track issues
critical_issues = []
warnings = []

# ============================================================================
# HEADER
# ============================================================================
print("=" * 70)
if FULL_MODE:
    print("🔍 VERIFICATION DASHBOARD - FULL DIAGNOSTIC CHECK")
else:
    print("🔍 VERIFICATION DASHBOARD - QUICK DIAGNOSTIC CHECK")
print("=" * 70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# ============================================================================
# 1. FILE STRUCTURE CHECK
# ============================================================================
print("📌 1. FILE STRUCTURE")
if FULL_MODE:
    print("-" * 70)

# Root files
print("📄 ROOT FILES:")
root_files = ['app.py', 'config.py', 'requirements.txt', '.env']
for file in root_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING!")
        critical_issues.append(f"Missing {file}")

# Utils folder
print("📁 UTILS FOLDER:")
utils_files = ['utils/', 'utils/__init__.py', 'utils/auth.py', 'utils/security.py', 'utils/pdf_generator.py']
for file in utils_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING!")
        critical_issues.append(f"Missing {file}")

# Templates folder
print("📁 TEMPLATES FOLDER:")
template_files = ['templates/', 'templates/index.html']
for file in template_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING!")
        critical_issues.append(f"Missing {file}")

# Static folders
print("📁 STATIC FOLDERS:")
static_folders = ['static/', 'static/css/', 'static/js/', 'static/view/', 'static/documents/']
for folder in static_folders:
    if os.path.exists(folder):
        print(f"✅ {folder}")
    else:
        print(f"❌ {folder} - MISSING!")
        critical_issues.append(f"Missing {folder}")

# Static files
print("📄 STATIC FILES:")
static_files = ['static/css/style.css', 'static/js/app.js']
for file in static_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING!")
        critical_issues.append(f"Missing {file}")

print()

# ============================================================================
# 2. DOCUMENT CHECK (11 DOCUMENTS)
# ============================================================================
print("📌 2. YOUR 11 DOCUMENTS")
if FULL_MODE:
    print("-" * 70)

# Check static/view/
print("static/view/:")
view_docs = []
if os.path.exists('static/view'):
    for doc in EXPECTED_DOCUMENTS:
        doc_path = os.path.join('static/view', doc)
        if os.path.exists(doc_path):
            print(f"   ✅ {doc}")
            view_docs.append(doc)
        else:
            print(f"   ❌ {doc} - MISSING!")
            critical_issues.append(f"Missing {doc} in static/view")
    print(f"   Found: {len(view_docs)}/11 documents")
else:
    print("   ❌ static/view folder not found!")
    critical_issues.append("static/view folder missing")

# Check static/documents/
print("static/documents/:")
download_docs = []
if os.path.exists('static/documents'):
    for doc in EXPECTED_DOCUMENTS:
        doc_path = os.path.join('static/documents', doc)
        if os.path.exists(doc_path):
            print(f"   ✅ {doc}")
            download_docs.append(doc)
        else:
            print(f"   ❌ {doc} - MISSING!")
            critical_issues.append(f"Missing {doc} in static/documents")
    print(f"   Found: {len(download_docs)}/11 documents")
else:
    print("   ❌ static/documents folder not found!")
    critical_issues.append("static/documents folder missing")

print()

# ============================================================================
# 3. ENVIRONMENT & PACKAGES CHECK
# ============================================================================
print("📌 3. ENVIRONMENT & PACKAGES")
if FULL_MODE:
    print("-" * 70)

# .env check
if os.path.exists('.env'):
    print("🔐 .env FILE:")
    try:
        with open('.env', 'r') as f:
            env_vars = []
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key = line.split('=')[0]
                    env_vars.append(key)
                    print(f"  ✅ {key} is set")
            
            # Check required variables
            required_vars = ['ACCESS_PASSWORD', 'SECRET_KEY', 'ADMIN_SECRET', 'FLASK_DEBUG']
            for var in required_vars:
                if var not in env_vars:
                    if var == 'FLASK_DEBUG':
                        warnings.append(f"{var} not found in .env (will use default)")
                    else:
                        warnings.append(f"{var} not found in .env")
    except Exception as e:
        print(f"  ⚠️  Could not read .env file: {e}")
        warnings.append("Could not read .env file")
else:
    print("❌ .env file missing!")
    critical_issues.append(".env file missing")

print()

# Package check
print("📦 PYTHON PACKAGES:")
required_packages = ['flask', 'flask_limiter', 'reportlab', 'python-dotenv', 'gunicorn', 'werkzeug']
missing_packages = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package}")
        if package == 'python-dotenv':
            warnings.append(f"{package} missing (optional)")
        else:
            missing_packages.append(package)
            critical_issues.append(f"Missing package: {package}")

if missing_packages:
    print(f"\n  Install: pip install {' '.join(missing_packages)}")

print()

# ============================================================================
# 4. CONFIG.PY VALIDATION
# ============================================================================
print("📌 4. CONFIG.PY VALIDATION")
if FULL_MODE:
    print("-" * 70)

print("🔍 CHECKING CONFIG ATTRIBUTES:")

if os.path.exists('config.py'):
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
            
            # Check for required attributes
            if 'FLASK_DEBUG' in config_content:
                print("✅ FLASK_DEBUG attribute found")
            else:
                critical_issues.append("FLASK_DEBUG attribute missing in config.py")
                print("❌ FLASK_DEBUG attribute MISSING!")
            
            if 'SECRET_KEY' in config_content:
                print("✅ SECRET_KEY attribute found")
            else:
                critical_issues.append("SECRET_KEY attribute missing in config.py")
                print("❌ SECRET_KEY attribute MISSING!")
            
            if 'DEMO_IDENTITY' in config_content:
                print("✅ DEMO_IDENTITY attribute found")
                
                # Check for both field name formats
                if ("'aadhaar':" in config_content or '"aadhaar":' in config_content) and \
                   ("'aadhaar_no':" in config_content or '"aadhaar_no":' in config_content):
                    print("✅ DEMO_IDENTITY has both field formats (aadhaar + aadhaar_no)")
                else:
                    warnings.append("DEMO_IDENTITY may be missing dual field formats")
                    print("⚠️ DEMO_IDENTITY may be missing dual field formats")
            else:
                critical_issues.append("DEMO_IDENTITY missing in config.py")
                print("❌ DEMO_IDENTITY MISSING!")
            
            if 'get_access_password' in config_content:
                print("✅ get_access_password() method found")
                
                # Check if it reads from .password_sync
                if '.password_sync' in config_content:
                    print("✅ Password sync integration present")
                else:
                    warnings.append("get_access_password may not read from .password_sync")
                    print("⚠️ Password sync integration may be missing")
            else:
                critical_issues.append("get_access_password method missing in config.py")
                print("❌ get_access_password() method MISSING!")
                
    except Exception as e:
        warnings.append(f"Could not read config.py: {e}")
        print(f"⚠️ Could not read config.py: {e}")
else:
    critical_issues.append("config.py file not found")
    print("❌ config.py file not found!")

print()

# ============================================================================
# 5. PASSWORD SYNC STATUS
# ============================================================================
print("📌 5. PASSWORD SYNC STATUS")
if FULL_MODE:
    print("-" * 70)

password_sync_file = '.password_sync'
if os.path.exists(password_sync_file):
    print(f"✅ Password sync file exists: {password_sync_file}")
    try:
        import json
        with open(password_sync_file, 'r') as f:
            data = json.load(f)
            if data.get('password'):
                print(f"✅ Password is synced from control panel")
                if data.get('updated_at'):
                    print(f"   Last updated: {data.get('updated_at')}")
                print(f"   Password length: {len(data.get('password'))} characters")
            else:
                warnings.append("Password sync file exists but no password found")
                print("⚠️ Password sync file exists but no password found")
    except Exception as e:
        warnings.append(f"Could not read password sync file: {e}")
        print(f"⚠️ Could not read password sync file: {e}")
else:
    print("ℹ️  Password sync file not found (.password_sync)")
    print("   This is normal if you haven't set a password in control panel yet")
    print("   Once you set password in control panel, this file will be created")

print()

# ============================================================================
# 6. UTILS MODULE VALIDATION
# ============================================================================
print("📌 6. UTILS MODULE VALIDATION")
if FULL_MODE:
    print("-" * 70)

print("🔧 CHECKING REQUIRED FUNCTIONS:")

# Check auth.py
try:
    from utils.auth import login_required
    print("✅ utils.auth.login_required found")
except ImportError as e:
    print(f"❌ utils.auth.login_required MISSING!")
    critical_issues.append("login_required function missing in utils/auth.py")

# Check security.py
try:
    from utils.security import validate_password
    print("✅ utils.security.validate_password found")
except ImportError as e:
    print(f"❌ utils.security.validate_password MISSING!")
    critical_issues.append("validate_password function missing in utils/security.py")

# Check pdf_generator.py
try:
    from utils.pdf_generator import generate_verification_report
    print("✅ utils.pdf_generator.generate_verification_report found")
except ImportError as e:
    print(f"❌ utils.pdf_generator.generate_verification_report MISSING!")
    critical_issues.append("generate_verification_report function missing in utils/pdf_generator.py")

print()

# ============================================================================
# 7. APP.PY VALIDATION
# ============================================================================
print("📌 7. APP.PY ROUTE VALIDATION")
if FULL_MODE:
    print("-" * 70)

print("🔍 CHECKING ROUTES AND IMPORTS:")

if os.path.exists('app.py'):
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            
            # Check imports
            if 'from utils.security import validate_password' in app_content:
                print("✅ validate_password import found")
            else:
                warnings.append("validate_password import may be missing")
                print("⚠️ validate_password import may be missing")
            
            # Check for generate_report route
            if '@app.route(\'/api/generate-report\')' in app_content:
                print("✅ /api/generate-report route exists")
                
                # Check for ID numbers in documents
                if "'id_number':" in app_content or '"id_number":' in app_content:
                    print("✅ Documents include 'id_number' field")
                else:
                    warnings.append("Documents may be missing 'id_number' field in generate_report")
                    print("⚠️ Documents may be missing 'id_number' field")
                
                # Check for all 11 documents
                doc_count = app_content.count("'verified': True")
                if doc_count >= 11:
                    print(f"✅ Found {doc_count} documents in generate_report")
                else:
                    warnings.append(f"Only {doc_count} documents found in generate_report (expected 11)")
                    print(f"⚠️ Only {doc_count} documents found (expected 11)")
            else:
                warnings.append("/api/generate-report route not found in app.py")
                print("⚠️ /api/generate-report route not found")
            
            # Check for password sync helpers
            if 'save_password_to_file' in app_content:
                print("✅ Password sync helper functions found")
            else:
                warnings.append("Password sync helper functions may be missing")
                print("⚠️ Password sync helper functions may be missing")
                
    except Exception as e:
        warnings.append(f"Could not read app.py: {e}")
        print(f"⚠️ Could not read app.py: {e}")
else:
    critical_issues.append("app.py file not found")
    print("❌ app.py file not found!")

print()

# ============================================================================
# 8. PDF GENERATOR VALIDATION
# ============================================================================
print("📌 8. PDF GENERATOR VALIDATION")
if FULL_MODE:
    print("-" * 70)

print("🔍 CHECKING PDF GENERATOR FOR ID COLUMN:")

if os.path.exists('utils/pdf_generator.py'):
    try:
        with open('utils/pdf_generator.py', 'r', encoding='utf-8') as f:
            pdf_content = f.read()
            
            # Check for ID number column
            if "'ID / Registration Number'" in pdf_content or '"ID / Registration Number"' in pdf_content:
                print("✅ PDF table includes 'ID / Registration Number' column")
            elif "'id_number'" in pdf_content or '"id_number"' in pdf_content:
                print("✅ PDF generator accesses 'id_number' field")
            else:
                warnings.append("PDF generator may not include ID numbers column")
                print("⚠️ PDF generator may not include ID numbers column")
            
            # Check for 5-column table
            if "colWidths=[0.4*inch, 2.2*inch, 1.5*inch, 2*inch, 0.9*inch]" in pdf_content:
                print("✅ PDF table configured for 5 columns (with ID numbers)")
            else:
                warnings.append("PDF table may not be configured for 5 columns")
                print("⚠️ PDF table may not be configured for 5 columns")
            
            # Check for SimpleDocTemplate
            if 'SimpleDocTemplate' in pdf_content:
                print("✅ Uses SimpleDocTemplate correctly")
            else:
                critical_issues.append("SimpleDocTemplate import may be missing")
                print("❌ SimpleDocTemplate import may be missing!")
                
    except Exception as e:
        warnings.append(f"Could not read pdf_generator.py: {e}")
        print(f"⚠️ Could not read pdf_generator.py: {e}")
else:
    critical_issues.append("utils/pdf_generator.py not found")
    print("❌ utils/pdf_generator.py not found!")

print()

# ============================================================================
# DIAGNOSTIC SUMMARY
# ============================================================================
print("=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)

if critical_issues:
    print(f"❌ CRITICAL ISSUES FOUND: {len(critical_issues)}")
    for issue in critical_issues:
        print(f"   • {issue}")
else:
    print("✅ ALL CHECKS PASSED! System is healthy!")
    if len(view_docs) == 11 and len(download_docs) == 11:
        print("✅ All 11 documents are in place!")

if warnings:
    print(f"\n⚠️  WARNINGS: {len(warnings)}")
    for warning in warnings:
        print(f"   • {warning}")

print("=" * 70)

# ============================================================================
# DEPLOYMENT STATUS
# ============================================================================
if not critical_issues:
    print("✅ READY FOR RENDER DEPLOYMENT 100% ✅")
    print("=" * 70)
    print("📂 DOCUMENT CATEGORIES:")
    print("   🆔 Government IDs: 3 documents")
    print("   🚗 Driving: 3 documents")
    print("   🎓 Educational: 2 documents")
    print("   📄 Professional: 2 documents")
    print("   📸 Personal: 1 document")
    print("=" * 70)
    print("🎊 ALL SYSTEMS GO! READY TO DEPLOY! 🚀")
else:
    print("⚠️  PLEASE FIX CRITICAL ISSUES BEFORE DEPLOYMENT")
    print("=" * 70)
    print("💡 RECOMMENDED FIXES:")
    print("=" * 70)
    for idx, issue in enumerate(critical_issues, 1):
        print(f"   {idx}. {issue}")
    print("=" * 70)

if not FULL_MODE:
    print("ℹ️  For detailed check, run: python diagnostic.py --full")

print("=" * 70)

# Exit with appropriate code
sys.exit(1 if critical_issues else 0)