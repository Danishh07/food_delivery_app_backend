from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime, time
from enum import Enum

class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_online: Optional[bool] = False
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_online: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True