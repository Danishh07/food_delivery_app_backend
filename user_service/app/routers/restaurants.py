from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
from app.database import get_db
from app.models.user import User
from app.schemas.restaurant import RestaurantBase, RestaurantDetail
from app.utils.auth import get_current_user
from app.utils.service_communication import get_restaurants, get_restaurant

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
    responses={401: {"description": "Unauthorized"}},
)

@router.get("/", response_model=List[RestaurantBase])
async def read_restaurants(
    hour: Optional[int] = Query(None, ge=0, le=23, description="Current hour (0-23)"),
    current_user: User = Depends(get_current_user)
):
    """
    Get all restaurants that are available online.
    Optionally filter by current hour to show only restaurants open at that time.
    """
    # If hour is not provided, use current hour
    if hour is None:
        now = datetime.datetime.now()
        hour = now.hour
    
    restaurants = await get_restaurants(hour)
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantDetail)
async def read_restaurant(
    restaurant_id: int, 
    current_user: User = Depends(get_current_user)
):
    """Get restaurant details including menu"""
    restaurant = await get_restaurant(restaurant_id)
    return restaurant
