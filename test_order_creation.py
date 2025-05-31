"""
Test script for creating an order in the Food Delivery App User Service
"""
import requests
import json

# Configuration
USER_SERVICE_URL = "http://localhost:8000"
RESTAURANT_SERVICE_URL = "http://localhost:8001" 

def register_user():
    """Register a new test user"""
    url = f"{USER_SERVICE_URL}/auth/register"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "555-123-4567",
        "address": "123 Test St"
    }
    
    response = requests.post(url, json=data)
    print(f"User Registration Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def get_auth_token(username="testuser", password="password123"):
    """Get authentication token"""
    url = f"{USER_SERVICE_URL}/auth/token"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, data=data)
    print(f"Auth Token Response: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token obtained: {token_data['access_token'][:20]}...")
        return token_data["access_token"]
    else:
        print(response.text)
        return None

def create_restaurant():
    """Create a test restaurant"""
    url = f"{RESTAURANT_SERVICE_URL}/restaurants"
    data = {
        "name": "Test Restaurant",
        "description": "A restaurant for testing",
        "address": "456 Test Ave",
        "phone_number": "555-987-6543",
        "email": "restaurant@example.com",
        "is_online": True,
        "opening_time": "09:00:00",
        "closing_time": "22:00:00"
    }
    
    response = requests.post(url, json=data)
    print(f"Restaurant Creation Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def add_menu_category(restaurant_id):
    """Add a menu category to a restaurant"""
    url = f"{RESTAURANT_SERVICE_URL}/restaurants/{restaurant_id}/menu-categories"
    data = {
        "name": "Test Category",
        "description": "Category for testing"
    }
    
    response = requests.post(url, json=data)
    print(f"Menu Category Creation Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def add_menu_item(restaurant_id, category_id):
    """Add a menu item to a category"""
    url = f"{RESTAURANT_SERVICE_URL}/restaurants/{restaurant_id}/menu-categories/{category_id}/items"
    data = {
        "name": "Test Item",
        "description": "A delicious test item",
        "price": 12.99,
        "is_available": True,
        "image_url": "https://example.com/test-item.jpg"
    }
    
    response = requests.post(url, json=data)
    print(f"Menu Item Creation Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def create_order(token, restaurant_id, menu_item_id):
    """Create an order in the User Service"""
    url = f"{USER_SERVICE_URL}/orders"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "restaurant_id": restaurant_id,
        "total_amount": 25.98,
        "order_items": [
            {
                "menu_item_id": menu_item_id,
                "quantity": 2,
                "notes": "Test order"
                # Intentionally omitting price to test the fix
            }
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Order Creation Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2) if response.status_code < 400 else response.text)
    return response.json() if response.status_code < 400 else None

def main():
    """Run the test flow"""
    # Step 1: Register a new user
    try:
        register_user()
    except Exception as e:
        print(f"User may already exist: {e}")
    
    # Step 2: Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to get token. Exiting...")
        return
    
    # Step 3: Create a restaurant
    restaurant = create_restaurant()
    if not restaurant:
        print("Failed to create restaurant. Exiting...")
        return
    
    # Step 4: Add a menu category
    category = add_menu_category(restaurant["id"])
    if not category:
        print("Failed to create menu category. Exiting...")
        return
    
    # Step 5: Add a menu item
    menu_item = add_menu_item(restaurant["id"], category["id"])
    if not menu_item:
        print("Failed to create menu item. Exiting...")
        return
    
    # Step 6: Create an order
    order = create_order(token, restaurant["id"], menu_item["id"])
    if order:
        print("Order created successfully!")
        print(f"Order ID: {order['id']}")
        print(f"Status: {order['status']}")
        print(f"Total Amount: ${order['total_amount']}")
    else:
        print("Failed to create order.")

if __name__ == "__main__":
    main()
