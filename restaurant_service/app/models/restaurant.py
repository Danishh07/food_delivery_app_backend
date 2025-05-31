from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Time, Numeric
from sqlalchemy.sql import func
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    __table_args__ = {"schema": "restaurant_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    address = Column(Text, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    is_online = Column(Boolean, default=False)
    opening_time = Column(Time)
    closing_time = Column(Time)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
