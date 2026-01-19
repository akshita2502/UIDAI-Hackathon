"""Main application entry point for UIDAI Sentinel fraud detection system"""  # noqa: E501

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from api_routes import router as api_router

# 1. Create DB Tables
models.Base.metadata.create_all(bind=engine)

# 2. Initialize FastAPI
app = FastAPI(title="UIDAI Sentinel - Fraud Detection System")
"""
UIDAI Sentinel: Real-time fraud detection system for Aadhaar enrolment anomalies.
Implements 6 different ML-based anomaly detection algorithms.
"""

# 3. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Mount API Routes
app.include_router(api_router)

# Run with: uvicorn main:app --reload
