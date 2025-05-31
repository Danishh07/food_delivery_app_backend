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
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int
    notes: Optional[str] = None
    price: Optional[float] = None

class OrderItemCreate(OrderItemBase):
    price: float

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    price: float
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    restaurant_id: int

class OrderCreate(OrderBase):
    order_items: List[OrderItemBase]
    total_amount: float

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime
    order_items: Optional[List[OrderItemResponse]] = None
    
    class Config:
        from_attributes = True
