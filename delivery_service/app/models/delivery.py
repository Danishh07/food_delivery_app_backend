from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class Delivery(Base):
    __tablename__ = "deliveries"
    __table_args__ = {"schema": "delivery_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    restaurant_order_id = Column(Integer, nullable=False)
    delivery_agent_id = Column(Integer, nullable=False)
    status = Column(String, default="assigned")  # assigned, picked_up, in_transit, delivered
    pickup_time = Column(DateTime(timezone=True))
    delivery_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())