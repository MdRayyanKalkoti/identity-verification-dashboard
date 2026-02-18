"""
Diagnostic Script - Check Verification Dashboard Setup
Run this to verify all files and folders are in place
"""

import os
import sys

def check_file(filepath, required=True):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌ REQUIRED" if required else "⚠️  OPTIONAL")
    print(f"{status} {filepath}")
    return exists

def check_folder(folderpath, required=True):
    """Check if folder exists"""
    exists = os.path.isdir(folderpath)
    status = "✅" if exists else ("❌ REQUIRED" if required else "⚠️  OPTIONAL")
    print(f"{status} {folderpath}/")
    return exists

def main():
    print("\n" + "="*70)
    print("🔍 VERIFICATION DASHBOARD - DIAGNOSTIC CHECK")
    print("="*70 + "\n")
    
    issues = []
    
    # Root files
    print("📄 ROOT FILES:")
    if not check_file('app.py'): issues.append('app.py missing')
    if not check_file('config.py'): issues.append('config.py missing')
    if not check_file('requirements.txt'): issues.append('requirements.txt missing')
    if not check_file('.env'): issues.append('.env missing')
    check_file('generate_pdfs_both_folders.py', required=False)
    print()
    
    # utils folder
    print("📁 UTILS FOLDER:")
    if not check_folder('utils'): issues.append('utils/ folder missing')
    if not check_file('utils/__init__.py'): issues.append('utils/__init__.py missing')
    if not check_file('utils/auth.py'): issues.append('utils/auth.py missing')
    if not check_file('utils/security.py'): issues.append('utils/security.py missing')
    if not check_file('utils/pdf_generator.py'): issues.append('utils/pdf_generator.py missing')
    print()
    
    # templates folder
    print("📁 TEMPLATES FOLDER:")
    if not check_folder('templates'): issues.append('templates/ folder missing')
    if not check_file('templates/index.html'): issues.append('templates/index.html missing')
    print()
    
    # static folders
    print("📁 STATIC FOLDERS:")
    if not check_folder('static'): issues.append('static/ folder missing')
    if not check_folder('static/css'): issues.append('static/css/ folder missing')
    if not check_folder('static/js'): issues.append('static/js/ folder missing')
    if not check_folder('static/view'): issues.append('static/view/ folder missing - CREATE THIS!')
    if not check_folder('static/documents'): issues.append('static/documents/ folder missing')
    print()
    
    # static files
    print("📄 STATIC FILES:")
    if not check_file('static/css/style.css'): issues.append('static/css/style.css missing')
    if not check_file('static/js/app.js'): issues.append('static/js/app.js missing')
    print()
    
    # PDF files in VIEW folder
    print("📄 VIEW FOLDER PDFs (for viewing in modal):")
    if not check_file('static/view/aadhaar_demo.pdf'): issues.append('static/view/aadhaar_demo.pdf missing')
    if not check_file('static/view/pan_demo.pdf'): issues.append('static/view/pan_demo.pdf missing')
    if not check_file('static/view/passport_demo.pdf'): issues.append('static/view/passport_demo.pdf missing')
    print()
    
    # PDF files in DOCUMENTS folder
    print("📄 DOCUMENTS FOLDER PDFs (for downloading):")
    if not check_file('static/documents/aadhaar_demo.pdf'): issues.append('static/documents/aadhaar_demo.pdf missing')
    if not check_file('static/documents/pan_demo.pdf'): issues.append('static/documents/pan_demo.pdf missing')
    if not check_file('static/documents/passport_demo.pdf'): issues.append('static/documents/passport_demo.pdf missing')
    print()
    
    # Summary
    print("="*70)
    if issues:
        print("❌ ISSUES FOUND:")
        print("="*70)
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print("\n⚠️  FIX THESE ISSUES BEFORE RUNNING THE APP")
    else:
        print("✅ ALL FILES AND FOLDERS ARE IN PLACE!")
        print("="*70)
        print("\n🚀 You can now run: python app.py")
    
    print("\n" + "="*70 + "\n")
    
    # Additional checks
    if os.path.exists('.env'):
        print("🔐 .env FILE CONTENTS:")
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key = line.split('=')[0]
                        print(f"  ✅ {key} is set")
        except:
            print("  ⚠️  Could not read .env file")
        print()
    
    # Check Python packages
    print("📦 CHECKING PYTHON PACKAGES:")
    required_packages = [
        'flask',
        'flask_limiter',
        'reportlab',
        'python-dotenv',
        'gunicorn',
        'werkzeug'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Run: pip install {package}")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()