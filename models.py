from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # admin / operator / user


class Ration(Base):
    __tablename__ = "rations"

    id = Column(Integer, primary_key=True, index=True)
    animal = Column(String)
    age = Column(Integer)
    goal = Column(String)
    data = Column(JSON)
    class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_phone = Column(String)
    class ConsumptionLog(Base):
    __tablename__ = "consumption_logs"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer)
    date = Column(String)
    data = Column(JSON)