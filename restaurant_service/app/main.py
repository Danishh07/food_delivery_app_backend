from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import restaurants, menu, orders
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery App - Restaurant Service",
    description="Restaurant Service for Food Delivery App",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Food Delivery App Restaurant Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
