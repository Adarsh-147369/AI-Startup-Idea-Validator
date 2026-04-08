import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import SessionLocal
from models import StartupIdea
from pdf_service import generate_pdf_report

router = APIRouter(prefix="/export", tags=["export"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{idea_id}")
def export_idea_pdf(idea_id: int, db: Session = Depends(get_db)):
    """
    Export a startup idea as an A4 PDF report.
    Returns a FileResponse with the PDF file.
    """
    idea = db.query(StartupIdea).filter(StartupIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Convert database model to dictionary
    idea_dict = {
        "id": idea.id,
        "idea_name": idea.idea_name,
        "idea_description": idea.idea_description,
        "problem": idea.problem,
        "customer": idea.customer,
        "market": idea.market,
        "competitors": json.loads(idea.competitors) if idea.competitors else [],
        "tech_stack": json.loads(idea.tech_stack) if idea.tech_stack else [],
        "risk_level": idea.risk_level,
        "profitability_score": idea.profitability_score,
        "ai_analysis": idea.ai_analysis,
        "created_at": idea.created_at,
        "updated_at": idea.updated_at
    }
    
    # Generate PDF
    pdf_content = generate_pdf_report(idea_dict)
    
    # Save to temporary file
    filename = f"startup_idea_{idea_id}.pdf"
    
    with open(filename, "wb") as f:
        f.write(pdf_content)
    
    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=f"startup_idea_{idea.idea_name.replace(' ', '_')}.pdf"
    )
