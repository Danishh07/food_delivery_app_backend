from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, time
from app.database import get_db
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.schemas.menu import MenuCategoryWithItems

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate, 
    db: Session = Depends(get_db)
):
    """Create a new restaurant"""
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.get("/", response_model=List[RestaurantResponse])
def read_restaurants(
    hour: Optional[int] = Query(None, ge=0, le=23, description="Current hour (0-23)"),
    is_online: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all restaurants.
    Filter by online status and/or current hour to show only restaurants open at that time.
    """
    query = db.query(Restaurant)
    
    # Filter by online status if provided
    if is_online is not None:
        query = query.filter(Restaurant.is_online == is_online)
    
    # Filter by hour if provided
    if hour is not None:
        # Convert hour to time
        current_time = time(hour=hour, minute=0)
        # Include restaurants where current time is between opening and closing times
        query = query.filter(
            Restaurant.opening_time <= current_time,
            Restaurant.closing_time >= current_time
        )
    
    restaurants = query.offset(skip).limit(limit).all()
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def read_restaurant(
    restaurant_id: int, 
    db: Session = Depends(get_db)
):
    """Get restaurant by ID"""
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int, 
    restaurant: RestaurantUpdate, 
    db: Session = Depends(get_db)
):
    """Update restaurant details"""
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Update restaurant fields if provided
    update_data = restaurant.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int, 
    db: Session = Depends(get_db)
):
    """Delete restaurant"""
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(db_restaurant)
    db.commit()
    return None