# VERIFICATION DASHBOARD - COMPLETE FILE CHECKLIST

## ✅ REQUIRED FILES AND FOLDERS

### Root Directory Files:
- [ ] app.py (updated with separate folders)
- [ ] config.py (with .env loading)
- [ ] requirements.txt
- [ ] .env (with ACCESS_PASSWORD)
- [ ] generate_pdfs_both_folders.py (optional)

### utils/ folder:
- [ ] utils/__init__.py (empty file)
- [ ] utils/auth.py
- [ ] utils/security.py (X-Frame-Options: SAMEORIGIN)
- [ ] utils/pdf_generator.py

### templates/ folder:
- [ ] templates/index.html (with PDF modal)

### static/css/ folder:
- [ ] static/css/style.css (with modal styles, z-index: 99999)

### static/js/ folder:
- [ ] static/js/app.js (with working modal code)

### static/view/ folder (NEW):
- [ ] static/view/aadhaar_demo.pdf
- [ ] static/view/pan_demo.pdf
- [ ] static/view/passport_demo.pdf

### static/documents/ folder:
- [ ] static/documents/aadhaar_demo.pdf
- [ ] static/documents/pan_demo.pdf
- [ ] static/documents/passport_demo.pdf

## 🔧 KEY CHANGES NEEDED:

1. app.py - Different folders for view vs download
2. security.py - X-Frame-Options: SAMEORIGIN (not DENY)
3. app.js - Correct modal opening code
4. style.css - Modal z-index: 99999
5. Both PDF folders must have files

## 🧪 TESTING CHECKLIST:

After setup:
- [ ] Server starts without errors
- [ ] Can unlock dashboard
- [ ] Click View → Modal opens
- [ ] PDF shows in modal (not blank)
- [ ] Click Download → PDF downloads
- [ ] Close button (X) works

## 📂 FOLDER STRUCTURE:

verification-dashboard/
├── .env
├── app.py
├── config.py
├── requirements.txt
├── generate_pdfs_both_folders.py
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── security.py
│   └── pdf_generator.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    ├── view/               ← FOR VIEWING
    │   ├── aadhaar_demo.pdf
    │   ├── pan_demo.pdf
    │   └── passport_demo.pdf
    └── documents/          ← FOR DOWNLOADING
        ├── aadhaar_demo.pdf
        ├── pan_demo.pdf
        └── passport_demo.pdf