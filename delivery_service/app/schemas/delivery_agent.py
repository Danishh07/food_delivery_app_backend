from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class DeliveryAgentStatus(str, Enum):
    inactive = "inactive"
    available = "available"
    busy = "busy"

class DeliveryAgentBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str
    status: DeliveryAgentStatus = DeliveryAgentStatus.inactive
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None

class DeliveryAgentCreate(DeliveryAgentBase):
    password: str

class DeliveryAgentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[DeliveryAgentStatus] = None
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    password: Optional[str] = None

class DeliveryAgentResponse(DeliveryAgentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DeliveryAgentPublic(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str
    status: DeliveryAgentStatus
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None