from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu import MenuCategory, MenuItem
from app.schemas.menu import (
    MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryResponse, MenuCategoryWithItems,
    MenuItemCreate, MenuItemUpdate, MenuItemResponse
)

router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
    responses={404: {"description": "Not found"}},
)

# Menu Categories Endpoints
@router.post("/categories", response_model=MenuCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: MenuCategoryCreate, 
    db: Session = Depends(get_db)
):
    """Create a new menu category"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == category.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db_category = MenuCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/restaurant/{restaurant_id}", response_model=List[MenuCategoryWithItems])
def read_categories_by_restaurant(
    restaurant_id: int, 
    db: Session = Depends(get_db)
):
    """Get all menu categories for a restaurant with their menu items"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Get all categories for the restaurant
    categories = db.query(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id).all()
    
    # For each category, get its menu items
    result = []
    for category in categories:
        items = db.query(MenuItem).filter(MenuItem.category_id == category.id).all()
        category_with_items = MenuCategoryWithItems(
            id=category.id,
            name=category.name,
            description=category.description,
            restaurant_id=category.restaurant_id,
            items=items
        )
        result.append(category_with_items)
    
    return result

@router.get("/categories/{category_id}", response_model=MenuCategoryWithItems)
def read_category(
    category_id: int, 
    db: Session = Depends(get_db)
):
    """Get a specific menu category with its menu items"""
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    items = db.query(MenuItem).filter(MenuItem.category_id == category_id).all()
    
    return MenuCategoryWithItems(
        id=category.id,
        name=category.name,
        description=category.description,
        restaurant_id=category.restaurant_id,
        items=items
    )

@router.put("/categories/{category_id}", response_model=MenuCategoryResponse)
def update_category(
    category_id: int, 
    category: MenuCategoryUpdate, 
    db: Session = Depends(get_db)
):
    """Update a menu category"""
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update category fields if provided
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db)
):
    """Delete a menu category"""
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return None

# Menu Items Endpoints
@router.post("/items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: MenuItemCreate, 
    db: Session = Depends(get_db)
):
    """Create a new menu item"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == item.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check if category exists if provided
    if item.category_id:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == item.category_id, 
            MenuCategory.restaurant_id == item.restaurant_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found or doesn't belong to this restaurant")
    
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/restaurant/{restaurant_id}", response_model=List[MenuItemResponse])
def read_items_by_restaurant(
    restaurant_id: int, 
    category_id: Optional[int] = None,
    available_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all menu items for a restaurant, optionally filtered by category or availability"""
    # Check if restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Base query
    query = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    
    # Filter by category if provided
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    
    # Filter by availability if requested
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    items = query.all()
    return items

@router.get("/items/{item_id}", response_model=MenuItemResponse)
def read_item(
    item_id: int, 
    db: Session = Depends(get_db)
):
    """Get a specific menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    return item

@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_item(
    item_id: int, 
    item: MenuItemUpdate, 
    db: Session = Depends(get_db)
):
    """Update a menu item"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check if category exists if provided
    if item.category_id:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == item.category_id, 
            MenuCategory.restaurant_id == db_item.restaurant_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found or doesn't belong to this restaurant")
    
    # Update item fields if provided
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db)
):
    """Delete a menu item"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(db_item)
    db.commit()
    return None