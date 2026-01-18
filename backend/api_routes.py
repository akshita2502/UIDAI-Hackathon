"""API Routes for UIDAI Sentinel - Fraud Detection System"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import ai_engine

router = APIRouter()

# --- ANALYTICS ROUTES ---


@router.get("/analytics/map-all")
def get_map_data(db: Session = Depends(get_db)):
    """Aggregated map data for all 6 anomalies"""
    return ai_engine.get_all_map_anomalies(db)


@router.get("/analytics/phantom-village")
def get_phantom_village_data(db: Session = Depends(get_db)):
    """Get Phantom Village anomaly data and chart visualization"""
    return ai_engine.analyze_phantom_village(db)["chart_data"]


@router.get("/analytics/update-mill")
def get_update_mill_data(db: Session = Depends(get_db)):
    """Get Update Mill anomaly data (unauthorized bulk operations)"""
    return ai_engine.analyze_update_mill(db)["chart_data"]


@router.get("/analytics/biometric-bypass")
def get_biometric_bypass_data(db: Session = Depends(get_db)):
    """Get Biometric Bypass anomaly data (incomplete verification)"""
    return ai_engine.analyze_biometric_bypass(db)["chart_data"]


@router.get("/analytics/scholarship-ghost")
def get_scholarship_ghost_data(db: Session = Depends(get_db)):
    """Get Scholarship Ghost anomaly data (child age/bio mismatch)"""
    return ai_engine.analyze_scholarship_ghost(db)["chart_data"]


@router.get("/analytics/bot-operator")
def get_bot_operator_data(db: Session = Depends(get_db)):
    """Get Bot Operator anomaly data (Benford's law violations)"""
    return ai_engine.analyze_bot_operator(db)["chart_data"]


@router.get("/analytics/sunday-shift")
def get_sunday_shift_data(db: Session = Depends(get_db)):
    """Get Sunday Shift anomaly data (temporal anomalies)"""
    return ai_engine.analyze_sunday_shift(db)["chart_data"]
