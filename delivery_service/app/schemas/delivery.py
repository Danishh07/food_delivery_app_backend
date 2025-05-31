from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class DeliveryStatus(str, Enum):
    assigned = "assigned"
    picked_up = "picked_up"
    in_transit = "in_transit"
    delivered = "delivered"
    cancelled = "cancelled"

class DeliveryBase(BaseModel):
    order_id: int
    restaurant_order_id: int
    delivery_agent_id: int

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    status: Optional[DeliveryStatus] = None
    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None

class DeliveryResponse(DeliveryBase):
    id: int
    status: DeliveryStatus
    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DeliveryLocationUpdate(BaseModel):
    latitude: float
    longitude: float