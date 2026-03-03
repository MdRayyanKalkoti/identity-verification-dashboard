# Shield Identity Verification Dashboard (rayyan-id)

A secure Flask web application for displaying verified identity documents. Protected by a password lock screen, with remote password management via webhook from the Control Panel.

## Project Structure

```
verification-dashboard/
├── app.py
├── config.py
├── diagnose.py
├── diagnostic.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── CHECKLIST.md
├── .env
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── security.py
│   └── pdf_generator.py
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    ├── js/app.js
    ├── view/
    │   ├── aadhaar_demo.pdf
    │   ├── pan_demo.pdf
    │   └── passport_demo.pdf
    └── documents/
        ├── aadhaar_demo.pdf
        ├── pan_demo.pdf
        └── passport_demo.pdf
```

## How It Works

User visits the site and sees a lock screen. After entering the correct ACCESS_PASSWORD, the dashboard unlocks giving access to four sections: Overview (stats and quick actions), Identity (personal info), Documents (view and download PDFs), and Reports (generate full PDF report).

The password can be updated remotely by the Control Panel via the `/api/admin/update-password` webhook with no restart required. All active sessions are force-logged out on password change.

## Setup and Running

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd verification-dashboard
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_flask_secret_key_here
ACCESS_PASSWORD=your_chosen_password
ADMIN_SECRET=same_value_as_control_panel
FLASK_DEBUG=False
```

| Variable | Description |
|---|---|
| SECRET_KEY | Flask session secret (auto-generated if not set) |
| ACCESS_PASSWORD | Password users enter to unlock the dashboard |
| ADMIN_SECRET | Shared secret for webhook auth with Control Panel |
| FLASK_DEBUG | Set False in production |

### 3. Add PDF Files

Place PDFs in both static folders:

```
static/view/aadhaar_demo.pdf       for viewing in modal
static/view/pan_demo.pdf
static/view/passport_demo.pdf

static/documents/aadhaar_demo.pdf  for downloading
static/documents/pan_demo.pdf
static/documents/passport_demo.pdf
```

### 4. Run the App

```bash
python app.py
```

Visit: http://localhost:5000

## Using the Dashboard

1. Visit the site — lock screen appears
2. Enter ACCESS_PASSWORD to unlock
3. Navigate via sidebar: Overview, Identity, Documents, Reports
4. Click View to open a PDF in the modal viewer
5. Click Download to download a PDF
6. Click Generate PDF Report for a full verification report
7. Click Logout or the session expires after 30 minutes

## Security Features

- Password lock screen — dashboard blurred and inaccessible until unlocked
- Session expiry — 30-minute sessions, auto-logout on expiry
- Force logout on password change — all active users logged out when password updated remotely
- HMAC timing-safe comparison — prevents timing attacks on password checks
- Rate limiting — password endpoint capped at 100/hour, webhook at 10/min
- Security headers — X-Frame-Options SAMEORIGIN, X-XSS-Protection, HSTS, CSP
- Webhook auth — /api/admin/update-password requires Bearer token matching ADMIN_SECRET

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /api/verify-password | None | Unlock the dashboard |
| POST | /api/logout | None | Log out current session |
| GET | /api/status | None | Check auth status and password-changed flag |
| POST | /api/acknowledge-password-change | None | Clear flag and force logout |
| GET | /api/identity | Session | Get identity data |
| GET | /api/documents/type | Session | Serve PDF document |
| GET | /api/generate-report | Session | Download full PDF report |
| POST | /api/admin/update-password | Bearer token | Update password remotely |

Document types: aadhaar, pan, passport

## Running Diagnostics

Quick structure check:
```bash
python diagnose.py
```

Full diagnostic report:
```bash
python diagnostic.py
```

The full diagnostic checks Python version, environment variables, required modules, file structure, PDF folders, config loading, auth system, security module, and PDF generator.

## Deploying to Render

1. Push repo to GitHub
2. Create a new Web Service on Render
3. Set Start Command: gunicorn app:app (from Procfile)
4. Set Runtime: python-3.11.0 (from runtime.txt)
5. Add environment variables under Environment: ACCESS_PASSWORD, SECRET_KEY, ADMIN_SECRET, FLASK_DEBUG=False

## Dependencies

| Package | Purpose |
|---|---|
| Flask | Web framework |
| Flask-Limiter | Rate limiting |
| gunicorn | Production WSGI server |
| reportlab | PDF report generation |
| python-dotenv | .env file loading |
| Werkzeug | Security utilities |
| Pillow | Image handling for PDFs |

## Common Issues

| Problem | Fix |
|---|---|
| Lock screen won't unlock | Check ACCESS_PASSWORD env var is set |
| PDF modal shows blank | Ensure files exist in static/view/ folder |
| PDF download fails | Ensure files exist in static/documents/ folder |
| Webhook returns 403 | ADMIN_SECRET mismatch with Control Panel |
| Sessions expire immediately | Set a strong SECRET_KEY env var |
| App crashes on start | Run python diagnose.py to find missing files |

## License

Internal tool — not for public distribution.