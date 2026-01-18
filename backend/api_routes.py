"""API routes for UIDAI Sentinel fraud detection analytics"""

import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import ai_engine

router = APIRouter()

# --- ANALYTICS ROUTES ---


@router.get("/analytics/map-all")
async def get_map_data(db: Session = Depends(get_db)):
    """Aggregated map data for all 6 anomalies (optimized parallel execution)"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ai_engine.get_all_map_anomalies, db)


@router.get("/analytics/phantom-village")
async def get_phantom_village_data(db: Session = Depends(get_db)):
    """Get Phantom Village anomaly data and chart visualization"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_phantom_village, db)
    return result["chart_data"]


@router.get("/analytics/update-mill")
async def get_update_mill_data(db: Session = Depends(get_db)):
    """Get Update Mill anomaly data (unauthorized bulk operations)"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_update_mill, db)
    return result["chart_data"]


@router.get("/analytics/biometric-bypass")
async def get_biometric_bypass_data(db: Session = Depends(get_db)):
    """Get Biometric Bypass anomaly data (incomplete verification)"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_biometric_bypass, db)
    return result["chart_data"]


@router.get("/analytics/scholarship-ghost")
async def get_scholarship_ghost_data(db: Session = Depends(get_db)):
    """Get Scholarship Ghost anomaly data (child age/bio mismatch)"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_scholarship_ghost, db)
    return result["chart_data"]


@router.get("/analytics/bot-operator")
async def get_bot_operator_data(db: Session = Depends(get_db)):
    """Get Bot Operator anomaly data (Benford's law violations)"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_bot_operator, db)
    return result["chart_data"]


@router.get("/analytics/sunday-shift")
async def get_sunday_shift_data(db: Session = Depends(get_db)):
    """Get Sunday Shift anomaly data (temporal anomalies)"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, ai_engine.analyze_sunday_shift, db)
    return result["chart_data"]
