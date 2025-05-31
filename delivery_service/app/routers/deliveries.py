from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.delivery_agent import DeliveryAgent
from app.models.delivery import Delivery
from app.schemas.delivery import (
    DeliveryCreate, DeliveryUpdate, DeliveryResponse, 
    DeliveryStatus, DeliveryLocationUpdate
)
from app.utils.auth import get_current_delivery_agent

router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    """Create a new delivery assignment"""
    # Check if delivery agent exists
    agent = db.query(DeliveryAgent).filter(DeliveryAgent.id == delivery.delivery_agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Delivery agent not found")
    
    # Check if delivery agent is available
    if agent.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery agent is not available"
        )
    
    # Create delivery
    db_delivery = Delivery(
        order_id=delivery.order_id,
        restaurant_order_id=delivery.restaurant_order_id,
        delivery_agent_id=delivery.delivery_agent_id,
        status="assigned"
    )
    
    # Update agent status to busy
    agent.status = "busy"
    
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.get("/agent/me", response_model=List[DeliveryResponse])
def get_my_deliveries(
    status: Optional[DeliveryStatus] = None,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Get all deliveries for the current delivery agent"""
    query = db.query(Delivery).filter(Delivery.delivery_agent_id == current_agent.id)
    
    if status:
        query = query.filter(Delivery.status == status)
    
    return query.all()

@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(
    delivery_id: int,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Get a specific delivery by ID"""
    delivery = db.query(Delivery).filter(
        Delivery.id == delivery_id, 
        Delivery.delivery_agent_id == current_agent.id
    ).first()
    
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    return delivery

@router.put("/{delivery_id}/status", response_model=DeliveryResponse)
def update_delivery_status(
    delivery_id: int,
    status: DeliveryStatus,
    current_agent: DeliveryAgent = Depends(get_current_delivery_agent),
    db: Session = Depends(get_db)
):
    """Update delivery status"""
    delivery = db.query(Delivery).filter(
        Delivery.id == delivery_id, 
        Delivery.delivery_agent_id == current_agent.id
    ).first()
    
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    # Update status based on the requested status and current status
    if status == DeliveryStatus.picked_up:
        if delivery.status != DeliveryStatus.assigned:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery must be in 'assigned' status to be picked up"
            )
        delivery.status = status
        delivery.pickup_time = datetime.now()
    
    elif status == DeliveryStatus.in_transit:
        if delivery.status != DeliveryStatus.picked_up:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery must be in 'picked_up' status to be in transit"
            )
        delivery.status = status
    
    elif status == DeliveryStatus.delivered:
        if delivery.status not in [DeliveryStatus.picked_up, DeliveryStatus.in_transit]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery must be in 'picked_up' or 'in_transit' status to be delivered"
            )
        delivery.status = status
        delivery.delivery_time = datetime.now()
        
        # Set delivery agent status back to available
        current_agent.status = "available"
    
    elif status == DeliveryStatus.cancelled:
        delivery.status = status
        
        # Set delivery agent status back to available
        current_agent.status = "available"
    
    db.commit()
    db.refresh(delivery)
    return delivery