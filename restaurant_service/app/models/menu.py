from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.sql import func
from app.database import Base

class MenuCategory(Base):
    __tablename__ = "menu_categories"
    __table_args__ = {"schema": "restaurant_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    
class MenuItem(Base):
    __tablename__ = "menu_items"
    __table_args__ = {"schema": "restaurant_service"}
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("restaurant_service.menu_categories.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(Text)
