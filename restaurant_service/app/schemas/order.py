from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    preparing = "preparing"
    ready_for_pickup = "ready_for_pickup"
    completed = "completed"
    cancelled = "cancelled"

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderBase(BaseModel):
    restaurant_id: int

class RestaurantOrderCreate(BaseModel):
    user_order_id: int
    restaurant_id: int
    order_items: List[OrderItemBase]
    
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    preparation_time: Optional[int] = None
    delivery_agent_id: Optional[int] = None

class OrderAssign(BaseModel):
    delivery_agent_id: int

class OrderResponse(BaseModel):
    id: int
    user_order_id: int
    restaurant_id: int
    delivery_agent_id: Optional[int] = None
    status: str
    preparation_time: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True