from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: Optional[bool] = True
    image_url: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    restaurant_id: int
    category_id: Optional[int] = None

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_id: int
    category_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class MenuCategoryCreate(MenuCategoryBase):
    restaurant_id: int

class MenuCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class MenuCategoryResponse(MenuCategoryBase):
    id: int
    restaurant_id: int
    
    class Config:
        from_attributes = True

class MenuCategoryWithItems(MenuCategoryResponse):
    items: List[MenuItemResponse] = []