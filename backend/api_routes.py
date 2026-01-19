"""API routes for UIDAI Sentinel fraud detection analytics"""

import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import ai_engine
from redis_client import get_cached_data, set_cached_data
from tasks import KEYS

router = APIRouter()


async def fetch_or_compute(
    cache_key: str,
    compute_func,
    background_tasks: BackgroundTasks,
    db: Session,
    is_map: bool = False,
):
    """Helper to check cache first, else compute in background"""
    # 1. Try Cache
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    # 2. Cache Miss: Compute immediately (blocking) so this user gets data
    # Alternatively, return empty and let background fill it (non-blocking)
    # We choose blocking for the first run to ensure data availability.
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, compute_func, db)

    # Extract correct data part
    data = result if is_map else result.get("chart_data")

    # 3. Update Cache in Background
    background_tasks.add_task(set_cached_data, cache_key, data)

    return data


@router.get("/analytics/map-all")
async def get_map_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch all map anomalies data"""
    return await fetch_or_compute(
        KEYS["map"], ai_engine.get_all_map_anomalies, background_tasks, db, is_map=True
    )


@router.get("/analytics/phantom-village")
async def get_phantom_village_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch phantom village anomaly data"""
    return await fetch_or_compute(
        KEYS["phantom"], ai_engine.analyze_phantom_village, background_tasks, db
    )


@router.get("/analytics/update-mill")
async def get_update_mill_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch update mill anomaly data"""
    return await fetch_or_compute(
        KEYS["update"], ai_engine.analyze_update_mill, background_tasks, db
    )


@router.get("/analytics/biometric-bypass")
async def get_biometric_bypass_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch biometric bypass anomaly data"""
    return await fetch_or_compute(
        KEYS["bio"], ai_engine.analyze_biometric_bypass, background_tasks, db
    )


@router.get("/analytics/scholarship-ghost")
async def get_scholarship_ghost_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch scholarship ghost anomaly data"""
    return await fetch_or_compute(
        KEYS["ghost"], ai_engine.analyze_scholarship_ghost, background_tasks, db
    )


@router.get("/analytics/bot-operator")
async def get_bot_operator_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch bot operator anomaly data"""
    return await fetch_or_compute(
        KEYS["bot"], ai_engine.analyze_bot_operator, background_tasks, db
    )


@router.get("/analytics/sunday-shift")
async def get_sunday_shift_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Fetch sunday shift anomaly data"""
    return await fetch_or_compute(
        KEYS["sunday"], ai_engine.analyze_sunday_shift, background_tasks, db
    )
