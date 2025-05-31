from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={401: {"description": "Unauthorized"}},
)

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(user: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user profile"""
    # Update user fields if provided
    if user.first_name is not None:
        current_user.first_name = user.first_name
    if user.last_name is not None:
        current_user.last_name = user.last_name
    if user.phone_number is not None:
        current_user.phone_number = user.phone_number
    if user.address is not None:
        current_user.address = user.address
    
    # Update the user in the database
    db.commit()
    db.refresh(current_user)
    return current_user
