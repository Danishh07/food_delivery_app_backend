import os
import httpx
from typing import Optional, Dict, Any, List

# Get service URLs from environment variables or use default
DELIVERY_SERVICE_URL = os.getenv("DELIVERY_SERVICE_URL", "http://localhost:8002")

async def get_available_delivery_agents():
    """Get all available delivery agents from the delivery service"""
    url = f"{DELIVERY_SERVICE_URL}/delivery-agents/available"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def assign_delivery_agent(order_id: int, delivery_agent_id: int):
    """Assign a delivery agent to an order"""
    url = f"{DELIVERY_SERVICE_URL}/deliveries"
    
    delivery_data = {
        "order_id": order_id,
        "delivery_agent_id": delivery_agent_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=delivery_data)
        response.raise_for_status()
        return response.json()