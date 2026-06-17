from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class AIHistory(Base):
    __tablename__ = "ai_history"

    id = Column(Integer, primary_key=True, index=True)

    animal = Column(String, nullable=False)
    goal = Column(String, nullable=False)

    score = Column(Float, nullable=False)

    ingredients = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)