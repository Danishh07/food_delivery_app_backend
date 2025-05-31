from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.utils.auth import get_current_user
from app.utils.service_communication import get_restaurant, create_restaurant_order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Create a new order"""
    # Check if restaurant exists
    restaurant = await get_restaurant(order.restaurant_id)
    
    # Check if restaurant is online
    if not restaurant["is_online"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant is currently offline"
        )
    
    # Create order in database
    db_order = Order(
        user_id=current_user.id,
        restaurant_id=order.restaurant_id,
        total_amount=order.total_amount,
        status="pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)    # Add order items
    for item in order.order_items:
        # Get price from the item if provided, otherwise calculate from menu
        price = getattr(item, 'price', None)
        if price is None:
            # Fetch price from restaurant menu via service communication
            restaurant_data = await get_restaurant(order.restaurant_id)
            found_price = False
            for category in restaurant_data.get("menu_categories", []):
                for menu_item in category.get("items", []):
                    if menu_item.get("id") == item.menu_item_id:
                        price = menu_item.get("price")
                        found_price = True
                        break
                if found_price:
                    break
            
            if price is None:
                # If we still couldn't find the price, set a default
                price = 0.0
        
        db_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price=price,
            notes=item.notes
        )
        db.add(db_item)
    
    db.commit()
    
    # Forward order to restaurant service
    restaurant_order_data = {
        "order_items": [{"menu_item_id": item.menu_item_id, "quantity": item.quantity} for item in order.order_items]
    }
    
    await create_restaurant_order(db_order.id, order.restaurant_id, restaurant_order_data)
    
    return db_order

@router.get("/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get order details by order ID"""
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return order
