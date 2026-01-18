"""Main application entry point for UIDAI Sentinel fraud detection system"""  # noqa: E501

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from socket_manager import sio
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

# 5. Mount Socket.IO
# This wraps the FastAPI app with the SocketIO ASGI app
app = socketio.ASGIApp(sio, app)

# Run with: uvicorn main:app --reload
