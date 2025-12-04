from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from database import Base

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String(100), nullable=True)
    basic_salary = Column(Float, nullable=False)
    bonus_percentage = Column(Float, nullable=False, default=0.0)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)  # Must match routes.py
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
