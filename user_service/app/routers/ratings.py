from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingResponse, RatingUpdate
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/", response_model=RatingResponse)
def create_rating(
    rating: RatingCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Create a rating for an order"""
    # Check if order exists and belongs to user
    order = db.query(Order).filter(Order.id == rating.order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found or doesn't belong to the user"
        )
    
    # Check if order status is delivered
    if order.status != "delivered":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Can only rate delivered orders"
        )
    
    # Check if rating already exists
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.order_id == rating.order_id
    ).first()
    
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Rating already exists for this order"
        )
    
    # Create new rating
    db_rating = Rating(
        user_id=current_user.id,
        order_id=rating.order_id,
        restaurant_rating=rating.restaurant_rating,
        delivery_rating=rating.delivery_rating,
        comments=rating.comments
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/", response_model=List[RatingResponse])
def read_ratings(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get all ratings for current user"""
    ratings = db.query(Rating).filter(Rating.user_id == current_user.id).offset(skip).limit(limit).all()
    return ratings

@router.put("/{rating_id}", response_model=RatingResponse)
def update_rating(
    rating_id: int,
    rating: RatingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing rating"""
    db_rating = db.query(Rating).filter(
        Rating.id == rating_id,
        Rating.user_id == current_user.id
    ).first()
    
    if not db_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Rating not found"
        )
    
    # Update rating
    if rating.restaurant_rating is not None:
        db_rating.restaurant_rating = rating.restaurant_rating
    if rating.delivery_rating is not None:
        db_rating.delivery_rating = rating.delivery_rating
    if rating.comments is not None:
        db_rating.comments = rating.comments
    
    db.commit()
    db.refresh(db_rating)
    return db_rating
