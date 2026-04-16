# ============================================
# TEST SCRIPT - Run this to verify PDF works
# ============================================
# Save as: test_pdf.py
# Run: python test_pdf.py

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

print("🔍 Testing PDF Generation...")
print("=" * 50)

# Test data
identity = {
    'name': 'Mohammad Rayyan Kalkoti',
    'dob': 'December 24, 2001',
    'nationality': 'Indian',
    'aadhaar': '4335 6189 7894',
    'pan': 'JKIPK0102E',
    'passport': 'Y2156864'
}

documents = [
    {'name': 'Aadhaar Card', 'category': 'Government ID', 'verified': True},
    {'name': 'PAN Card', 'category': 'Government ID', 'verified': True},
]

print("✅ Step 1: Creating buffer...")
buffer = BytesIO()

print("✅ Step 2: Creating PDF document...")
doc = SimpleDocTemplate(buffer, pagesize=A4)
print(f"   Type of doc: {type(doc)}")
print(f"   Is SimpleDocTemplate? {type(doc).__name__ == 'SimpleDocTemplate'}")

print("✅ Step 3: Creating elements...")
elements = []
styles = getSampleStyleSheet()

title = Paragraph("TEST REPORT", styles['Heading1'])
elements.append(title)

print("✅ Step 4: Building PDF...")
try:
    doc.build(elements)
    print("✅ SUCCESS! PDF built successfully!")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"   Type of doc: {type(doc)}")
    import sys
    sys.exit(1)

print("✅ Step 5: Saving test file...")
buffer.seek(0)
with open('test_report.pdf', 'wb') as f:
    f.write(buffer.read())

print()
print("=" * 50)
print("🎉 SUCCESS! PDF Generated!")
print("📄 File saved as: test_report.pdf")
print("   Open it to verify it works!")
print("=" * 50)