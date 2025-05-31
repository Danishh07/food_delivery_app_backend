from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time

class MenuItemBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool

class MenuCategoryBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    items: List[MenuItemBase]

class RestaurantBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: str
    is_online: bool
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantDetail(RestaurantBase):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    menu_categories: Optional[List[MenuCategoryBase]] = None
