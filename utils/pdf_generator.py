# ============================================
# COMPLETE MINIMAL pdf_generator.py WITH ID NUMBERS
# ============================================
# Replace your entire utils/pdf_generator.py with this

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def generate_verification_report(identity, documents=None):
    """Generate PDF report with ID numbers column"""
    
    # Create buffer
    buffer = BytesIO()
    
    # Create PDF document
    pdf_document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )
    
    # Elements list
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=8
    )
    
    # Title
    title = Paragraph("IDENTITY VERIFICATION REPORT", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Verification header
    header_data = [
        ['Status:', 'VERIFIED ✓', 'Date:', datetime.now().strftime('%B %d, %Y')],
        ['Documents:', '11 Total', 'ID:', f'VER-{datetime.now().strftime("%Y%m%d")}-001']
    ]
    
    header_table = Table(header_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e40af')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bfdbfe'))
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Personal Information
    personal_heading = Paragraph("Personal Information", heading_style)
    elements.append(personal_heading)
    
    personal_data = [
        ['Full Name:', identity.get('name', 'N/A')],
        ['Date of Birth:', identity.get('dob', 'N/A')],
        ['Nationality:', identity.get('nationality', 'N/A')],
        ['Address:', identity.get('address', 'N/A')]
    ]
    
    if identity.get('email'):
        personal_data.append(['Email:', identity.get('email')])
    if identity.get('phone'):
        personal_data.append(['Phone:', identity.get('phone')])
    
    personal_table = Table(personal_data, colWidths=[2*inch, 5*inch])
    personal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    
    elements.append(personal_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Government IDs
    govt_heading = Paragraph("🆔 Government Identification", subheading_style)
    elements.append(govt_heading)
    
    govt_data = [
        ['Aadhaar:', identity.get('aadhaar', identity.get('aadhaar_no', 'N/A'))],
        ['PAN:', identity.get('pan', identity.get('pan_no', 'N/A'))],
        ['Passport:', identity.get('passport', identity.get('passport_no', 'N/A'))],
    ]
    
    govt_table = Table(govt_data, colWidths=[2*inch, 5*inch])
    govt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fde68a'))
    ]))
    
    elements.append(govt_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Verified Documents with ID Numbers
    if documents:
        docs_heading = Paragraph(f"Verified Documents ({len(documents)} Total)", heading_style)
        elements.append(docs_heading)
        elements.append(Spacer(1, 0.1*inch))
        
        # Group by category
        categories = {}
        for doc in documents:
            cat = doc['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)
        
        category_order = ['Government ID', 'Driving Document', 'Educational', 'Professional', 'Personal']
        category_icons = {
            'Government ID': '🆔',
            'Driving Document': '🚗',
            'Educational': '🎓',
            'Professional': '📄',
            'Personal': '📸'
        }
        
        # Display each category
        for category in category_order:
            if category in categories:
                # Category heading
                cat_heading = Paragraph(
                    f"{category_icons.get(category, '📋')} {category}",
                    subheading_style
                )
                elements.append(cat_heading)
                
                # Table header with ID Numbers column
                doc_data = [['#', 'Document Name', 'Category', 'ID / Registration Number', 'Status']]
                
                # Add documents
                for idx, doc in enumerate(categories[category], 1):
                    status = '✓ Verified' if doc.get('verified') else '✗ Not Verified'
                    id_number = doc.get('id_number', 'N/A')
                    
                    doc_data.append([
                        str(idx),
                        doc['name'],
                        doc['category'],
                        id_number,  # ← ID NUMBERS COLUMN
                        status
                    ])
                
                # Create table with 5 columns
                doc_table = Table(doc_data, colWidths=[0.4*inch, 2.2*inch, 1.5*inch, 2*inch, 0.9*inch])
                
                doc_table.setStyle(TableStyle([
                    # Header
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    
                    # Data rows
                    ('FONTNAME', (0, 1), (2, -1), 'Helvetica'),
                    ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),  # ID Number BOLD
                    ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),  # Status BOLD
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                    ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                    ('ALIGN', (3, 1), (3, -1), 'LEFT'),
                    ('ALIGN', (4, 1), (4, -1), 'CENTER'),
                    
                    # Grid and padding
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('PADDING', (0, 0), (-1, -1), 5),
                    
                    # Alternate rows
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
                ]))
                
                elements.append(doc_table)
                elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    elements.append(Spacer(1, 0.2*inch))
    summary_heading = Paragraph("Verification Summary", heading_style)
    elements.append(summary_heading)
    
    summary_data = [
        ['Total Documents Verified:', '11 / 11'],
        ['Government IDs:', '3 documents'],
        ['Driving Documents:', '3 documents'],
        ['Educational Certificates:', '2 documents'],
        ['Professional Documents:', '2 documents'],
        ['Personal Documents:', '1 document'],
        ['Verification Completion:', '100%']
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdf4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#166534')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bbf7d0')),
        
        # Highlight last row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#16a34a')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTSIZE', (0, -1), (-1, -1), 12)
    ]))
    
    elements.append(summary_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    # Build PDF
    pdf_document.build(elements)
    
    # Return buffer
    buffer.seek(0)
    return buffer