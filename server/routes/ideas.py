import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import StartupIdea
from schemas import IdeaCreate, IdeaResponse
from ai_service import validate_idea

router = APIRouter(prefix="/api/ideas", tags=["ideas"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=IdeaResponse)
def create_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    """
    Create a new startup idea and validate it using AI.
    Only requires idea_name and idea_description.
    AI generates: problem, customer, market, competitors, tech_stack, risk_level, profitability_score
    """
    # Create initial database entry
    db_idea = StartupIdea(
        idea_name=idea.idea_name,
        idea_description=idea.idea_description
    )
    db.add(db_idea)
    db.commit()
    db.refresh(db_idea)
    
    # Validate idea with AI - AI generates all fields
    validation_result = validate_idea(idea.dict())
    
    # Update database with AI-generated fields
    db_idea.problem = validation_result.get("problem")
    db_idea.customer = validation_result.get("customer")
    db_idea.market = validation_result.get("market")
    db_idea.competitors = json.dumps(validation_result.get("competitors", []))
    db_idea.tech_stack = json.dumps(validation_result.get("tech_stack", []))
    db_idea.risk_level = validation_result.get("risk_level")
    db_idea.profitability_score = validation_result.get("profitability_score")
    db_idea.ai_analysis = validation_result.get("ai_analysis")
    
    db.commit()
    db.refresh(db_idea)
    
    # Parse JSON strings back to lists for response
    response_data = IdeaResponse(
        id=db_idea.id,
        idea_name=db_idea.idea_name,
        idea_description=db_idea.idea_description,
        problem=db_idea.problem,
        customer=db_idea.customer,
        market=db_idea.market,
        competitors=json.loads(db_idea.competitors) if db_idea.competitors else [],
        tech_stack=json.loads(db_idea.tech_stack) if db_idea.tech_stack else [],
        risk_level=db_idea.risk_level,
        profitability_score=db_idea.profitability_score,
        ai_analysis=db_idea.ai_analysis,
        created_at=db_idea.created_at,
        updated_at=db_idea.updated_at
    )
    
    return response_data


@router.get("/", response_model=List[IdeaResponse])
def get_ideas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all startup ideas with pagination.
    """
    ideas = db.query(StartupIdea).offset(skip).limit(limit).all()
    
    result = []
    for idea in ideas:
        result.append(IdeaResponse(
            id=idea.id,
            idea_name=idea.idea_name,
            idea_description=idea.idea_description,
            problem=idea.problem,
            customer=idea.customer,
            market=idea.market,
            competitors=json.loads(idea.competitors) if idea.competitors else [],
            tech_stack=json.loads(idea.tech_stack) if idea.tech_stack else [],
            risk_level=idea.risk_level,
            profitability_score=idea.profitability_score,
            ai_analysis=idea.ai_analysis,
            created_at=idea.created_at,
            updated_at=idea.updated_at
        ))
    
    return result


@router.get("/{idea_id}", response_model=IdeaResponse)
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """
    Get a specific startup idea by ID.
    """
    idea = db.query(StartupIdea).filter(StartupIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    return IdeaResponse(
        id=idea.id,
        idea_name=idea.idea_name,
        idea_description=idea.idea_description,
        problem=idea.problem,
        customer=idea.customer,
        market=idea.market,
        competitors=json.loads(idea.competitors) if idea.competitors else [],
        tech_stack=json.loads(idea.tech_stack) if idea.tech_stack else [],
        risk_level=idea.risk_level,
        profitability_score=idea.profitability_score,
        ai_analysis=idea.ai_analysis,
        created_at=idea.created_at,
        updated_at=idea.updated_at
    )


@router.delete("/{idea_id}")
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    """
    Delete a startup idea by ID.
    """
    idea = db.query(StartupIdea).filter(StartupIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    db.delete(idea)
    db.commit()
    
    return {"message": "Idea deleted successfully"}
