from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, JSON, BigInteger, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# --- Enums for Standardization ---
class SeverityLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AnomalyType(str, enum.Enum):
    PHANTOM_VILLAGE = "Phantom Village"     # Fake IDs
    UPDATE_MILL = "Update Mill"             # Bulk Operations
    BIO_BYPASS = "Biometric Bypass"         # Incomplete Verification
    SCHOLARSHIP_GHOST = "Scholarship Ghost" # Child Mismatch
    SUNDAY_SHIFT = "Sunday Shift"           # Temporal Fraud
    BOT_OPERATOR = "Bot Operator"           # Pattern Fabrication
    CLONE_CENTER = "Clone Center"           # Duplicate Data
    FLASH_MOB = "Flash Mob"                 # Spike Detection
    ZOMBIE_DISTRICT = "Zombie District"     # Input-Only

# --- 1. Raw Data Tables (Ingestion Layer) ---

class EnrolmentData(Base):
    __tablename__ = "enrolment_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    pincode = Column(Integer, index=True)
    
    # The Metrics
    age_0_5 = Column(Integer, default=0)
    age_5_17 = Column(Integer, default=0)
    age_18_greater = Column(Integer, default=0)

    # Composite Index for faster Time-Series + Location queries
    __table_args__ = (Index('idx_enrol_pin_date', "pincode", "date"),)

class DemographicData(Base):
    __tablename__ = "demographic_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    pincode = Column(Integer, index=True)

    # The Metrics
    demo_age_5_17 = Column(Integer, default=0)
    demo_age_17_ = Column(Integer, default=0)

    __table_args__ = (Index('idx_demo_pin_date', "pincode", "date"),)

class BiometricData(Base):
    __tablename__ = "biometric_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    pincode = Column(Integer, index=True)

    # The Metrics
    bio_age_5_17 = Column(Integer, default=0)
    bio_age_17_ = Column(Integer, default=0)

    __table_args__ = (Index('idx_bio_pin_date', "pincode", "date"),)

# --- 2. The Intelligence Layer (Alerts) ---

class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Where and When
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    data_date = Column(Date, nullable=False) # The date the anomaly actually happened
    pincode = Column(Integer, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)

    # What happened
    anomaly_type = Column(Enum(AnomalyType), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    description = Column(String, nullable=False) # Human readable summary
    
    # Technical Proof (Stored as JSON for flexibility)
    # Example: {"z_score": 45.2, "expected": 2, "actual": 500}
    evidence = Column(JSON, nullable=True) 
    
    # Status (For the dashboard UI to "Dismiss" or "Investigate" alerts)
    status = Column(String, default="OPEN") # OPEN, INVESTIGATING, RESOLVED