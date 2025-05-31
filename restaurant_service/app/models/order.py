from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "restaurant_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    user_order_id = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    delivery_agent_id = Column(Integer)
    status = Column(String, default="pending")
    preparation_time = Column(Integer)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
