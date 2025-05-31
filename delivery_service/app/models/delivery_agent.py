from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
from app.database import Base

class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"
    __table_args__ = {"schema": "delivery_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, nullable=False)
    status = Column(String, default="inactive")  # inactive, available, busy
    current_latitude = Column(Numeric(10, 8))
    current_longitude = Column(Numeric(11, 8))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())