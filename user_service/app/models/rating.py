from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        CheckConstraint('restaurant_rating BETWEEN 1 AND 5', name='check_restaurant_rating'),
        CheckConstraint('delivery_rating BETWEEN 1 AND 5', name='check_delivery_rating'),
        {"schema": "user_service"}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    restaurant_rating = Column(Integer)
    delivery_rating = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
