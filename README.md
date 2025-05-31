# Food Delivery App Backend

A microservice-based backend system for a food delivery application built with Python, FastAPI, PostgreSQL, and Docker.

## Services

The application consists of three main microservices:

1. **User Service** - Handles user authentication, restaurant discovery, order placement, and ratings
2. **Restaurant Service** - Manages restaurant information, menus, and order processing
3. **Delivery Agent Service** - Manages delivery agent status and delivery tracking

## Tech Stack

- **Backend**: Python 3.9+ with FastAPI
- **Database**: PostgreSQL
- **API Documentation**: OpenAPI (Swagger)
- **Containerization**: Docker and Docker Compose
- **API Testing**: Postman Collection included

## Architecture

This project follows a microservice architecture pattern with three separate services that communicate via RESTful APIs:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   User Service  │◄───►│Restaurant Service│◄───►│ Delivery Service│
│   (Port 8000)   │     │   (Port 8001)   │     │   (Port 8002)   │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         └─────────────►│                 │◄─────────────┘
                        │   PostgreSQL    │
                        │    Database     │
                        │                 │
                        └─────────────────┘
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register a new user using the `/auth/register` endpoint
2. Login with your credentials at `/auth/token` endpoint to receive an access token
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

All endpoints except `/auth/register` and `/auth/token` require authentication.

### Running the Application Locally

1. Clone the repository
   ```
   git clone https://github.com/yourusername/food-delivery-app.git
   cd food-delivery-app
   ```

2. Start the services using Docker Compose
   ```
   docker-compose up -d
   ```

3. Initialize the database (only needed first time)
   ```
   # PostgreSQL initialization happens automatically via the init.sql script in docker-compose
   ```

4. Access the services:
   - User Service: http://localhost:8000/docs
   - Restaurant Service: http://localhost:8001/docs
   - Delivery Agent Service: http://localhost:8002/docs
   
5. Use Postman collection for API testing
   - Import the `postman_collection.json` file into Postman
   - Set environment variables for the service URLs if needed


## Project Structure

```
food_delivery_app/
├── docker-compose.yml
├── init.sql                # Database initialization script
├── user_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       ├── routers/
│       └── utils/
├── restaurant_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       ├── routers/
│       └── utils/
├── delivery_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       ├── routers/
│       └── utils/
└── postman_collection.json # API testing collection
```

## Database Schema

The database is divided into three schemas, one for each microservice:

### User Service Schema

- **users**: Stores user information
  - id (PK), username, email, password_hash, first_name, last_name, phone_number, address, created_at, updated_at

- **orders**: Stores order information from the user perspective
  - id (PK), user_id, restaurant_id, total_amount, status, created_at, updated_at

- **order_items**: Stores items for each order
  - id (PK), order_id, menu_item_id, quantity, price, notes

- **ratings**: Stores user ratings for restaurants and delivery agents
  - id (PK), user_id, order_id, restaurant_rating, delivery_rating, comments, created_at

### Restaurant Service Schema

- **restaurants**: Stores restaurant information
  - id (PK), name, description, address, phone_number, email, is_online, opening_time, closing_time, created_at, updated_at

- **menu_categories**: Stores menu categories for restaurants
  - id (PK), restaurant_id, name, description

- **menu_items**: Stores menu items for restaurants
  - id (PK), restaurant_id, category_id (FK), name, description, price, is_available, image_url

- **orders**: Stores order information from the restaurant perspective
  - id (PK), user_order_id, restaurant_id, delivery_agent_id, status, preparation_time, created_at, updated_at

### Delivery Service Schema

- **delivery_agents**: Stores delivery agent information
  - id (PK), username, email, password_hash, first_name, last_name, phone_number, status, current_latitude, current_longitude, created_at, updated_at

- **deliveries**: Stores delivery information
  - id (PK), order_id, restaurant_order_id, delivery_agent_id, status, pickup_time, delivery_time, created_at, updated_at

## API Testing

Import the included Postman collection to test all available endpoints.

### Example API Usage

#### Creating an Order in User Service
To create an order, use the following request format:

```json
POST /orders
{
  "restaurant_id": 1,
  "total_amount": 25.98,
  "order_items": [
    {
      "menu_item_id": 1,
      "quantity": 2,
      "notes": "Extra cheese please",
      "price": 12.99  // Price is optional, system will fetch from restaurant menu if not provided
    }
  ]
}
```

Note: You do not need to include `user_id` in your request. It is automatically determined from your authentication token.

## Deployment

The services can be deployed individually to platforms like Heroku or as a complete stack using a container orchestration service.

### Deployment to Render

1. Create a Render account at [render.com](https://render.com) if you don't have one.

2. Connect your GitHub repository to Render (or use the provided `render.yaml` file).

3. Deploy using Blueprint (easiest):
   - Fork or push your repository to GitHub
   - In the Render Dashboard, click "New" and select "Blueprint"
   - Connect to your GitHub repo
   - Render will automatically detect the `render.yaml` file and configure all services

4. Alternatively, deploy services individually:
   - Create a PostgreSQL database in Render
   - Create web services for each microservice (user, restaurant, delivery)
   - Use the provided Dockerfiles for each service
   - Set the appropriate environment variables:
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `RESTAURANT_SERVICE_URL`: URL to your restaurant service
     - `DELIVERY_SERVICE_URL`: URL to your delivery service

5. Initialize the database:
   - Connect to your Render PostgreSQL database
   - Run the `init.sql` script using the provided `render_deploy.sh` script

6. Access your deployed services:
   - User Service: https://food-delivery-user-service.onrender.com/docs
   - Restaurant Service: https://food-delivery-restaurant-service.onrender.com/docs
   - Delivery Service: https://food-delivery-delivery-service.onrender.com/docs