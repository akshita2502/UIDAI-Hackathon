from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import ai_engine

router = APIRouter()

# --- ANALYTICS ROUTES (Visualization Data) ---

@router.get("/analytics/phantom-village")
def get_phantom_village_data(db: Session = Depends(get_db)):
    """Returns data for: Fake ID Generation Ring (Isolation Forest)"""
    return ai_engine.analyze_phantom_village(db)

@router.get("/analytics/update-mill")
def get_update_mill_data(db: Session = Depends(get_db)):
    """Returns data for: Unauthorized Bulk Operations (Z-Score)"""
    return ai_engine.analyze_update_mill(db)

@router.get("/analytics/biometric-bypass")
def get_biometric_bypass_data(db: Session = Depends(get_db)):
    """Returns data for: High Demographic / Zero Biometric updates"""
    return ai_engine.analyze_biometric_bypass(db)

@router.get("/analytics/scholarship-ghost")
def get_scholarship_ghost_data(db: Session = Depends(get_db)):
    """Returns data for: Child Age/Bio Mismatch"""
    return ai_engine.analyze_scholarship_ghost(db)

@router.get("/analytics/bot-operator")
def get_bot_operator_data(db: Session = Depends(get_db)):
    """Returns data for: Round Number Patterns (Benford's Law)"""
    return ai_engine.analyze_bot_operator(db)

@router.get("/analytics/sunday-shift")
def get_sunday_shift_data(db: Session = Depends(get_db)):
    """Returns data for: Temporal Fraud (Sunday Activity)"""
    return ai_engine.analyze_sunday_shift(db)