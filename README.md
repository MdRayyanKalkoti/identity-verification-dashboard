# Identity Verification Dashboard

A secure, KYC-style verification dashboard for professional CV enhancement.

## Features
- Password-protected access
- Professional dashboard UI
- Document management (view/download)
- PDF report generation
- Session-based authentication

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
1. Clone repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create demo PDFs in `static/documents/`:
   - aadhaar_demo.pdf
   - pan_demo.pdf
   - passport_demo.pdf

4. Run application:
```bash
   python app.py
```

5. Access at `http://localhost:5000`
6. Password will be displayed in console

## Deployment on Render

### Steps:
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Set environment variables:
   - `SECRET_KEY`
   - `ACCESS_PASSWORD` (optional, auto-generated if not set)

### Environment Variables
- `SECRET_KEY`: Flask secret key (auto-generated if not set)
- `ACCESS_PASSWORD`: Dashboard access password (auto-generated if not set)
- `FLASK_DEBUG`: Set to `False` for production

## Security Notes
- All data is demo/sample only
- No real sensitive information should be used
- Session-based authentication with 30-minute timeout
- Rate limiting on password attempts
- Security headers enabled

## Tech Stack
- Backend: Flask 3.0
- Frontend: HTML/CSS/JavaScript
- PDF Generation: ReportLab
- Session Management: Flask-Session
- Production Server: Gunicorn

## License
Private/Proprietary - For CV demonstration purposes only