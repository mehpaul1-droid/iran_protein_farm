from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import JSON

DATABASE_URL = "sqlite:///./farm_ai.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class RationHistory(Base):
    __tablename__ = "ration_history"

    id = Column(Integer, primary_key=True, index=True)
    animal = Column(String)
    age = Column(Integer)
    goal = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)