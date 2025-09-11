from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.api import api_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="RenewMart API",
    description="Land Management System API",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to RenewMart API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RenewMart API"}

@app.get("/api/v1/health")
async def api_health_check():
    return {"status": "healthy", "service": "RenewMart API", "version": "1.0.0"}
