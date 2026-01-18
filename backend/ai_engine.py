import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import models
from pandas import Series

def get_dataframe(db: Session, model_class):
    """Helper to convert SQL table to Pandas DataFrame"""
    query = db.query(model_class)
    conn = db.bind
    if conn is None:
        raise ValueError("Database connection is not available")
    return pd.read_sql(query.statement, conn)

# --- 1. THE PHANTOM VILLAGE (Fake ID Ring) ---
def analyze_phantom_village(db: Session):
    """
    Detects spikes in Adult Enrolment (age_18_greater) using Isolation Forest.
    Returns: List of anomalies.
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty: return []

    # ML Logic: Isolation Forest
    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly'] = model.fit_predict(df[['age_18_greater']].fillna(0))
    
    # Filter Anomalies (-1)
    anomalies = df[df['anomaly'] == -1].copy()
    anomalies['severity'] = 'CRITICAL'
    
    # Format for API
    return anomalies[['date', 'state', 'district', 'pincode', 'age_18_greater', 'severity']].to_dict(orient='records')

# --- 2. THE UPDATE MILL (Unauthorized Bulk Ops) ---
def analyze_update_mill(db: Session):
    """
    Detects statistical outliers in Demographic Updates (demo_age_17_).
    Returns: Top suspect pincodes.
    """
    df = get_dataframe(db, models.DemographicData)
    if df.empty: return []

    # Logic: Z-Score Outlier Detection
    # Calculate Mean/Std per District to account for local population differences
    stats = df.groupby('district')['demo_age_17_'].transform(lambda x: (x - x.mean()) / x.std())
    df['z_score'] = stats.fillna(0)
    
    # Threshold: Z > 3 (3 Standard Deviations away)
    suspects = df[df['z_score'] > 3].sort_values(by='z_score', ascending=False)
    
    return suspects[['date', 'district', 'pincode', 'demo_age_17_', 'z_score']].head(50).to_dict(orient='records')

# --- 3. THE BIOMETRIC BYPASS (Incomplete Verification) ---
def analyze_biometric_bypass(db: Session):
    """
    Finds Pincodes with High Demographic Updates but Near-Zero Biometric Updates.
    """
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty: return []

    # Merge on Location + Date
    merged = pd.merge(demo_df, bio_df, on=['date', 'state', 'district', 'pincode'])
    
    # Logic: High Ratio of Demo to Bio
    # Filter: Significant activity (Demo > 50) but suspicious Bio (< 10% of Demo)
    suspects = merged[
        (merged['demo_age_17_'] > 50) & 
        (merged['bio_age_17_'] < (merged['demo_age_17_'] * 0.1))
    ].copy()
    
    suspects['risk_score'] = suspects['demo_age_17_'] / (suspects['bio_age_17_'] + 1)
    
    return suspects.sort_values('risk_score', ascending=False).head(50).to_dict(orient='records')

# --- 4. THE SCHOLARSHIP GHOST (Child Age/Bio Mismatch) ---
def analyze_scholarship_ghost(db: Session):
    """
    Detects districts where Child Demographic updates > Child Biometric updates.
    (Implies changing age/details without child present).
    """
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty: return []

    merged = pd.merge(demo_df, bio_df, on=['date', 'state', 'district', 'pincode'])
    
    # Logic: Ratio mismatch for 5-17 age group
    suspects = merged[
        (merged['demo_age_5_17'] > 20) & 
        (merged['bio_age_5_17'] < 5)
    ].copy()
    
    return suspects[['date', 'district', 'pincode', 'demo_age_5_17', 'bio_age_5_17']].to_dict(orient='records')

# --- 5. THE BOT OPERATOR (Benford's Law / Round Numbers) ---
def analyze_bot_operator(db: Session):
    """
    Checks if enrolment counts are suspiciously 'round' (ending in 0 or 5).
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty: return []

    # Logic: Calculate % of 'Round Numbers' per Pincode
    df['is_round'] = df['age_18_greater'].apply(lambda x: 1 if x > 0 and x % 5 == 0 else 0)
    
    pincode_stats = df.groupby('pincode').agg(
        total_days=('date', 'count'),
        round_count=('is_round', 'sum')
    ).reset_index()
    
    pincode_stats['round_pct'] = (pincode_stats['round_count'] / pincode_stats['total_days']) * 100
    
    # Filter: > 80% round numbers is unnatural
    bots = pincode_stats[
        (pincode_stats['total_days'] > 5) & 
        (pincode_stats['round_pct'] > 80)
    ].sort_values('round_pct', ascending=False)
    
    return bots.to_dict(orient='records')

# --- 6. THE SUNDAY SHIFT (Temporal Anomaly) ---
def analyze_sunday_shift(db: Session):
    """
    Detects high activity on Sundays (when centers should be closed).
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty: return []

    # Logic: Filter for Sundays (weekday == 6) and high volume
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].apply(lambda x: x.weekday())
    
    sundays = df[
        (df['weekday'] == 6) & 
        (df['age_18_greater'] > 10) # Threshold for 'suspicious' Sunday
    ].copy()
    
    sundays['date'] = sundays['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    return sundays.sort_values('age_18_greater', ascending=False).to_dict(orient='records')