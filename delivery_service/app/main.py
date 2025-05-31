from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import delivery_agents, deliveries
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery App - Delivery Service",
    description="Delivery Service for Food Delivery App",
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
app.include_router(delivery_agents.router)
app.include_router(deliveries.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Food Delivery App Delivery Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}