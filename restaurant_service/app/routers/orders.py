from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.order import Order
from app.schemas.order import (
    OrderStatus, RestaurantOrderCreate, OrderUpdate, 
    OrderResponse, OrderAssign
)
from app.utils.service_communication import get_available_delivery_agents, assign_delivery_agent
import random

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)

async def auto_assign_delivery_agent(db: Session, order_id: int):
    """Background task to automatically assign a delivery agent to an order"""
    # Get the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.status != "accepted":
        return
    
    try:
        # Get available delivery agents
        available_agents = await get_available_delivery_agents()
        
        if not available_agents:
            print(f"No delivery agents available for order {order_id}")
            return
        
        # Randomly select an available agent
        selected_agent = random.choice(available_agents)
        
        # Assign the delivery agent to the order
        order.delivery_agent_id = selected_agent["id"]
        db.commit()
        
        # Notify delivery service
        await assign_delivery_agent(order.id, selected_agent["id"])
        
        print(f"Assigned delivery agent {selected_agent['id']} to order {order_id}")
    except Exception as e:
        print(f"Error assigning delivery agent to order {order_id}: {str(e)}")

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: RestaurantOrderCreate, 
    db: Session = Depends(get_db)
):
    """Create a new order in the restaurant service"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check if restaurant is online
    if not restaurant.is_online:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant is currently offline"
        )
    
    # Create order
    db_order = Order(
        user_order_id=order.user_order_id,
        restaurant_id=order.restaurant_id,
        status="pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/restaurant/{restaurant_id}", response_model=List[OrderResponse])
def read_orders_by_restaurant(
    restaurant_id: int, 
    status: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all orders for a restaurant, optionally filtered by status"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Base query
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int, 
    db: Session = Depends(get_db)
):
    """Get order details by order ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return order

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    
    # Update order fields if provided
    if order_update.status:
        order.status = order_update.status
    if order_update.preparation_time is not None:
        order.preparation_time = order_update.preparation_time
    if order_update.delivery_agent_id is not None:
        order.delivery_agent_id = order_update.delivery_agent_id
    
    # If order is accepted, auto-assign a delivery agent
    if order_update.status == OrderStatus.accepted:
        background_tasks.add_task(auto_assign_delivery_agent, db, order_id)
    
    db.commit()
    db.refresh(order)
    return order

@router.put("/{order_id}/assign-delivery", response_model=OrderResponse)
async def assign_delivery_to_order(
    order_id: int,
    order_assign: OrderAssign,
    db: Session = Depends(get_db)
):
    """Manually assign a delivery agent to an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    
    # Assign delivery agent
    order.delivery_agent_id = order_assign.delivery_agent_id
    db.commit()
    
    # Notify delivery service
    await assign_delivery_agent(order.id, order_assign.delivery_agent_id)
    
    db.refresh(order)
    return order