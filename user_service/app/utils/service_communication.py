import os
import httpx
from typing import Optional, Dict, Any

# Get service URLs from environment variables or use default
RESTAURANT_SERVICE_URL = os.getenv("RESTAURANT_SERVICE_URL", "http://localhost:8001")
DELIVERY_SERVICE_URL = os.getenv("DELIVERY_SERVICE_URL", "http://localhost:8002")

async def get_restaurants(hour: Optional[int] = None):
    """Get all restaurants from the restaurant service"""
    url = f"{RESTAURANT_SERVICE_URL}/restaurants"
    if hour is not None:
        url = f"{url}?hour={hour}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def get_restaurant(restaurant_id: int):
    """Get restaurant details from the restaurant service"""
    url = f"{RESTAURANT_SERVICE_URL}/restaurants/{restaurant_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def create_restaurant_order(user_order_id: int, restaurant_id: int, data: Dict[str, Any]):
    """Create order in restaurant service"""
    url = f"{RESTAURANT_SERVICE_URL}/orders"
    order_data = {
        "user_order_id": user_order_id,
        "restaurant_id": restaurant_id,
        **data
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=order_data)
        response.raise_for_status()
        return response.json()
