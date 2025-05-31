from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, restaurants, orders, ratings
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery App - User Service",
    description="User Service for Food Delivery App",
    version="1.0.0",
)

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend local development
    "https://food-delivery-app.onrender.com",  # Main frontend (if deployed)
    "https://food-delivery-user-service.onrender.com",
    "https://food-delivery-restaurant-service.onrender.com",
    "https://food-delivery-delivery-service.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(orders.router)
app.include_router(ratings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Food Delivery App User Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
