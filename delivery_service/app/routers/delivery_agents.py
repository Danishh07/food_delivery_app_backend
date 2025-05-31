from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.database import get_db
from app.models.delivery_agent import DeliveryAgent
from app.schemas.delivery_agent import (
    DeliveryAgentCreate, DeliveryAgentUpdate, DeliveryAgentResponse,
    DeliveryAgentPublic, Token, DeliveryAgentStatus
)
from app.utils.auth import (
    authenticate_delivery_agent, create_access_token, get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_delivery_agent
)

router = APIRouter(
    prefix="/delivery-agents",
    tags=["Delivery Agents"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/register", response_model=DeliveryAgentResponse)
def register_delivery_agent(agent: DeliveryAgentCreate, db: Session = Depends(get_db)):
    """Register a new delivery agent"""
    # Check if username already exists
    db_agent = db.query(DeliveryAgent).filter(DeliveryAgent.username == agent.username).first()
    if db_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Check if email already exists
    db_agent = db.query(DeliveryAgent).filter(DeliveryAgent.email == agent.email).first()
    if db_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new delivery agent
    hashed_password = get_password_hash(agent.password)
    db_agent = DeliveryAgent(
        username=agent.username,
        email=agent.email,
        password_hash=hashed_password,
        first_name=agent.first_name,
        last_name=agent.last_name,
        phone_number=agent.phone_number,
        status=agent.status,
        current_latitude=agent.current_latitude,
        current_longitude=agent.current_longitude,
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Get access token for delivery agent"""
    agent = authenticate_delivery_agent(db, form_data.username, form_data.password)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": agent.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=DeliveryAgentResponse)
def read_agent_me(current_agent: DeliveryAgent = Depends(get_current_delivery_agent)):
    """Get current delivery agent profile"""
    return current_agent

@router.put("/me", response_model=DeliveryAgentResponse)
def update_agent_me(
    agent: DeliveryAgentUpdate,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Update current delivery agent profile"""
    # Update agent fields if provided
    if agent.first_name is not None:
        current_agent.first_name = agent.first_name
    if agent.last_name is not None:
        current_agent.last_name = agent.last_name
    if agent.phone_number is not None:
        current_agent.phone_number = agent.phone_number
    if agent.status is not None:
        current_agent.status = agent.status
    if agent.current_latitude is not None:
        current_agent.current_latitude = agent.current_latitude
    if agent.current_longitude is not None:
        current_agent.current_longitude = agent.current_longitude
    if agent.password is not None:
        current_agent.password_hash = get_password_hash(agent.password)
    
    db.commit()
    db.refresh(current_agent)
    return current_agent

@router.put("/me/status/{status}", response_model=DeliveryAgentResponse)
def update_agent_status(
    status: DeliveryAgentStatus,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Update delivery agent status (inactive, available, busy)"""
    current_agent.status = status
    db.commit()
    db.refresh(current_agent)
    return current_agent

@router.put("/me/location", response_model=DeliveryAgentResponse)
def update_agent_location(
    latitude: float,
    longitude: float,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Update delivery agent current location"""
    current_agent.current_latitude = latitude
    current_agent.current_longitude = longitude
    db.commit()
    db.refresh(current_agent)
    return current_agent

@router.get("/available", response_model=List[DeliveryAgentPublic])
def get_available_agents(db: Session = Depends(get_db)):
    """Get all available delivery agents"""
    return db.query(DeliveryAgent).filter(DeliveryAgent.status == "available").all()