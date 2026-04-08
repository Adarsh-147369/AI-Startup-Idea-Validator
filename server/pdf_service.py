import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io


def generate_pdf_report(idea: dict, output_path: str = None) -> bytes:
    """
    Generate an A4 PDF report for a startup idea.
    
    Args:
        idea: Dictionary containing idea details
        output_path: Optional path to save the PDF. If None, returns bytes.
        
    Returns:
        PDF content as bytes if output_path is None, otherwise None
    """
    buffer = io.BytesIO() if output_path is None else output_path
    
    doc = SimpleDocTemplate(
        buffer if output_path is None else output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#1a1a1a')
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        leading=14
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Startup Idea Validation Report", title_style))
    story.append(Spacer(1, 20))
    
    # Idea Name
    story.append(Paragraph(idea.get('idea_name', 'N/A'), styles['Heading1']))
    story.append(Spacer(1, 20))
    
    # Idea Description
    story.append(Paragraph("Idea Description", heading_style))
    story.append(Paragraph(idea.get('idea_description', 'N/A'), normal_style))
    story.append(Spacer(1, 20))
    
    # Scores Section
    profitability_score = idea.get('profitability_score', 0)
    risk_level = idea.get('risk_level', 'Unknown')
    
    score_data = [
        ["Profitability Score:", f"{profitability_score}/100"],
        ["Risk Level:", risk_level]
    ]
    
    score_table = Table(score_data, colWidths=[2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#dbeafe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(score_table)
    story.append(Spacer(1, 20))
    
    # Problem
    if idea.get('problem'):
        story.append(Paragraph("Problem", heading_style))
        story.append(Paragraph(idea.get('problem', 'N/A'), normal_style))
        story.append(Spacer(1, 15))
    
    # Customer
    if idea.get('customer'):
        story.append(Paragraph("Target Customer", heading_style))
        story.append(Paragraph(idea.get('customer', 'N/A'), normal_style))
        story.append(Spacer(1, 15))
    
    # Market
    if idea.get('market'):
        story.append(Paragraph("Market Analysis", heading_style))
        story.append(Paragraph(idea.get('market', 'N/A'), normal_style))
        story.append(Spacer(1, 15))
    
    # Competitors
    competitors = idea.get('competitors', [])
    if competitors:
        story.append(Paragraph("Competitors", heading_style))
        for comp in competitors:
            story.append(Paragraph(f"• {comp}", normal_style))
        story.append(Spacer(1, 15))
    
    # Tech Stack
    tech_stack = idea.get('tech_stack', [])
    if tech_stack:
        story.append(Paragraph("Recommended Tech Stack", heading_style))
        for tech in tech_stack:
            story.append(Paragraph(f"• {tech}", normal_style))
        story.append(Spacer(1, 15))
    
    # AI Analysis
    ai_analysis = idea.get('ai_analysis')
    if ai_analysis:
        try:
            analysis_data = json.loads(ai_analysis) if isinstance(ai_analysis, str) else ai_analysis
            
            # Strengths
            strengths = analysis_data.get('strengths', [])
            if strengths:
                story.append(Paragraph("Strengths", heading_style))
                for strength in strengths:
                    story.append(Paragraph(f"• {strength}", normal_style))
                story.append(Spacer(1, 15))
            
            # Weaknesses
            weaknesses = analysis_data.get('weaknesses', [])
            if weaknesses:
                story.append(Paragraph("Weaknesses", heading_style))
                for weakness in weaknesses:
                    story.append(Paragraph(f"• {weakness}", normal_style))
                story.append(Spacer(1, 15))
            
            # Recommendations
            recommendations = analysis_data.get('recommendations', [])
            if recommendations:
                story.append(Paragraph("Recommendations", heading_style))
                for rec in recommendations:
                    story.append(Paragraph(f"• {rec}", normal_style))
                story.append(Spacer(1, 15))
            
            # Overall Analysis
            overall_analysis = analysis_data.get('overall_analysis', '')
            if overall_analysis:
                story.append(Paragraph("Overall Analysis", heading_style))
                story.append(Paragraph(overall_analysis, normal_style))
                
        except (json.JSONDecodeError, TypeError):
            pass
    
    story.append(Spacer(1, 30))
    
    # Footer
    created_at = idea.get('created_at', datetime.utcnow())
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except:
            created_at = datetime.utcnow()
    
    footer_text = f"Generated on {created_at.strftime('%Y-%m-%d %H:%M:%S')} | AI Startup Idea Validator"
    story.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )))
    
    # Build PDF
    doc.build(story)
    
    if output_path is None:
        buffer.seek(0)
        return buffer.getvalue()
    
    return None
