from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class IdeaCreate(BaseModel):
    idea_name: str
    idea_description: str


class IdeaResponse(BaseModel):
    id: int
    idea_name: str
    idea_description: str
    problem: Optional[str] = None
    customer: Optional[str] = None
    market: Optional[str] = None
    competitors: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    risk_level: Optional[str] = None
    profitability_score: Optional[float] = None
    ai_analysis: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True