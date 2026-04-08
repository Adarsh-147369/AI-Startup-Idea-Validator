from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from datetime import datetime
from database import Base


class StartupIdea(Base):
    __tablename__ = "startup_ideas"

    id = Column(Integer, primary_key=True, index=True)
    idea_name = Column(String, index=True)
    idea_description = Column(Text)
    problem = Column(Text, nullable=True)
    customer = Column(Text, nullable=True)
    market = Column(Text, nullable=True)
    competitors = Column(JSON, nullable=True)
    tech_stack = Column(JSON, nullable=True)
    risk_level = Column(String, nullable=True)
    profitability_score = Column(Float, nullable=True)
    ai_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)