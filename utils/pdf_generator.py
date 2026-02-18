from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_verification_report(identity_data):
    """Generate comprehensive verification report"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    title = Paragraph("IDENTITY VERIFICATION REPORT", title_style)
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    # Verification Badge
    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#10b981'),
        alignment=1,
        spaceAfter=20
    )
    badge = Paragraph("✓ VERIFIED", badge_style)
    story.append(badge)
    story.append(Spacer(1, 0.3*inch))
    
    # Identity Information Table
    identity_table_data = [
        ['Field', 'Value'],
        ['Full Name', identity_data['name']],
        ['Aadhaar Number', identity_data['aadhaar']],
        ['PAN Number', identity_data['pan']],
        ['Passport Number', identity_data['passport']],
        ['Date of Birth', identity_data['dob']],
        ['Verification Status', identity_data['verification_status']],
        ['Verification Date', identity_data['verification_date']]
    ]
    
    identity_table = Table(identity_table_data, colWidths=[2.5*inch, 3.5*inch])
    identity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(identity_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Documents Section
    doc_title = Paragraph("VERIFIED DOCUMENTS", styles['Heading2'])
    story.append(doc_title)
    story.append(Spacer(1, 0.2*inch))
    
    documents_data = [
        ['Document Type', 'Status', 'Format'],
        ['Aadhaar Card', '✓ Available', 'PDF'],
        ['PAN Card', '✓ Available', 'PDF'],
        ['Passport', '✓ Available', 'PDF']
    ]
    
    doc_table = Table(documents_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    doc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(doc_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    footer = Paragraph(
        f"Generated: {timestamp} | FOR DEMONSTRATION PURPOSES ONLY | All data is sample/demo data",
        footer_style
    )
    story.append(Spacer(1, 0.3*inch))
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer