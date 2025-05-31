from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import time

class RatingBase(BaseModel):
    restaurant_rating: Optional[int] = Field(None, ge=1, le=5)
    delivery_rating: Optional[int] = Field(None, ge=1, le=5)
    comments: Optional[str] = None

class RatingCreate(RatingBase):
    user_id: int
    order_id: int

class RatingUpdate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    user_id: int
    order_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
