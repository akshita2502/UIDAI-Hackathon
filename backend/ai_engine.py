"""AI engine module for UIDAI Sentinel fraud detection algorithms"""

import random
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
import models


def get_dataframe(db: Session, model_class):
    """Helper to convert SQL table to Pandas DataFrame"""
    query = db.query(model_class)
    conn = db.bind
    if conn is None:
        raise ValueError("Database connection is not available")
    return pd.read_sql(query.statement, conn)


# --- 1. PHANTOM VILLAGE (Fake ID Ring) ---
def analyze_phantom_village(db: Session):
    """
    Detects Phantom Village (Fake ID Ring) anomalies using Isolation Forest.

    Returns dictionary with:
    - chart_data: State-wise breakdown of anomalies vs normal registrations
    - map_data: Geographic distribution of critical anomalies
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    # Isolation Forest
    model = IsolationForest(contamination=0.01, random_state=42)
    df["anomaly"] = model.fit_predict(df[["age_18_greater"]].fillna(0))

    # 1. Chart Data: State-wise Anomalies
    # Group by state and count anomalies vs normal
    state_stats = df.groupby(["state", "anomaly"]).size().unstack(fill_value=0)
    # Rename columns: -1 is Anomaly, 1 is Normal
    if -1 in state_stats.columns:
        state_stats = state_stats.rename(
            columns={-1: "anomaly_count", 1: "normal_count"}
        )
    else:
        state_stats["anomaly_count"] = 0
        state_stats = state_stats.rename(columns={1: "normal_count"})

    chart_data = state_stats.reset_index()[
        ["state", "anomaly_count", "normal_count"]
    ].to_dict(orient="records")

    # 2. Map Data: Critical Anomalies
    anomalies = df[df["anomaly"] == -1].copy()
    anomalies["severity"] = "CRITICAL"
    anomalies["type"] = "Phantom Village"
    map_data = anomalies[
        ["pincode", "district", "state", "age_18_greater", "severity", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 2. UPDATE MILL (Unauthorized Bulk Ops) ---
def analyze_update_mill(db: Session):
    """
    Detects Update Mill (Unauthorized Bulk Operations) anomalies.
    Uses Z-Score outlier detection on demographic updates per district.

    Returns dictionary with:
    - chart_data: District-wise z-score distribution
    - map_data: Geographic hotspots of suspicious activities
    """
    df = get_dataframe(db, models.DemographicData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    # Z-Score Calculation
    stats = df.groupby("district")["demo_age_17_"].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    df["z_score"] = stats.fillna(0)

    # Filter for Chart (Top 20 suspicious districts)
    top_districts = (
        df[["district", "z_score"]]
        .drop_duplicates()
        .sort_values("z_score", ascending=False)
        .head(20)
    )
    chart_data = top_districts.to_dict(orient="records")

    # Filter for Map (Z-Score > 3)
    suspects = df[df["z_score"] > 3].copy()
    suspects["type"] = "Update Mill"
    map_data = suspects[
        ["pincode", "district", "state", "z_score", "demo_age_17_", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 3. BIOMETRIC BYPASS (Incomplete Verification) ---
def analyze_biometric_bypass(db: Session):
    """
    Detects Biometric Bypass (Incomplete Verification) anomalies.
    Identifies pincodes with high demographic updates but low biometric updates.

    Returns dictionary with:
    - chart_data: Risk score distribution and scatter plot data
    - map_data: Geographic visualization of bypass attempts
    """
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty:
        return {"chart_data": [], "map_data": []}

    merged = pd.merge(demo_df, bio_df, on=["date", "state", "district", "pincode"])

    # Risk Score
    merged["risk_score"] = merged["demo_age_17_"] / (merged["bio_age_17_"] + 1)

    # 1. Chart Data: Scatter Plot (Sample 200 points to avoid browser lag)
    chart_data = (
        merged[["demo_age_17_", "bio_age_17_", "risk_score"]]
        .sample(min(200, len(merged)))
        .to_dict(orient="records")
    )

    # 2. Map Data: High Risk
    high_risk = merged[merged["risk_score"] > 5].copy()  # Threshold
    high_risk["type"] = "Biometric Bypass"
    map_data = high_risk[
        ["pincode", "district", "state", "risk_score", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 4. SCHOLARSHIP GHOST (Child Age/Bio Mismatch) ---
def analyze_scholarship_ghost(db: Session):
    """
    Detects Scholarship Ghost (Child Age/Bio Mismatch) anomalies.
    Identifies districts where child demographic updates exceed biometric updates.

    Returns dictionary with:
    - chart_data: District-wise child demographic vs biometric comparison
    - map_data: Geographic distribution of mismatches
    """
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty:
        return {"chart_data": [], "map_data": []}

    merged = pd.merge(demo_df, bio_df, on=["date", "state", "district", "pincode"])

    # Group by District
    district_stats = (
        merged.groupby("district")[["demo_age_5_17", "bio_age_5_17"]]
        .sum()
        .reset_index()
    )

    # Calculate Mismatch Ratio
    district_stats["mismatch_ratio"] = district_stats["demo_age_5_17"] / (
        district_stats["bio_age_5_17"] + 1
    )

    # 1. Chart Data: Top 10 Mismatched Districts
    chart_data = (
        district_stats.sort_values("mismatch_ratio", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

    # 2. Map Data
    map_data = []

    return {"chart_data": chart_data, "map_data": map_data}


# --- 5. BOT OPERATOR (Benford's Law) ---
def analyze_bot_operator(db: Session):
    """
    Detects Bot Operator (Benfords Law or Round Numbers) anomalies.
    Identifies pincodes with suspiciously high percentages of round numbers.

    Returns dictionary with:
    - chart_data: Percentage distribution of round vs non-round enrolments
    - map_data: Top suspicious pincodes ranked by round number percentage
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    df["is_round"] = df["age_18_greater"].apply(
        lambda x: 1 if x > 0 and x % 5 == 0 else 0
    )

    pincode_stats = (
        df.groupby("pincode")
        .agg(total_days=("date", "count"), round_count=("is_round", "sum"))
        .reset_index()
    )

    pincode_stats["round_pct"] = (
        pincode_stats["round_count"] / pincode_stats["total_days"]
    ) * 100

    # 1. Chart Data: Pie Chart Counts
    suspicious_count = len(pincode_stats[pincode_stats["round_pct"] > 80])
    natural_count = len(pincode_stats) - suspicious_count

    chart_data = [
        {"name": "Suspicious (>80% Round)", "value": suspicious_count},
        {"name": "Natural", "value": natural_count},
    ]

    # 2. Map Data
    bots = pincode_stats[pincode_stats["round_pct"] > 80].copy()
    bots["type"] = "Bot Operator"
    # We need to merge back state/district info which was lost in groupby
    # For efficiency, we just take the pincode list
    map_data = bots[["pincode", "type", "round_pct"]].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 6. SUNDAY SHIFT (Temporal Anomaly) ---
def analyze_sunday_shift(db: Session):
    """
    Detects Sunday Shift (Temporal Anomaly) anomalies.
    Identifies high activity on Sundays when enrolment centers should be closed.

    Returns dictionary with:
    - chart_data: Weekly activity trend showing day-of-week patterns
    - map_data: Specific pincodes with Sunday anomalies
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].apply(lambda x: x.strftime("%A"))

    # 1. Chart Data: Avg Enrolment per Day
    # Sort order: Mon -> Sun
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    daily_stats = (
        df.groupby("day_of_week")["age_18_greater"]
        .mean()
        .reindex(days_order)
        .reset_index()
    )
    chart_data = daily_stats.to_dict(orient="records")

    # 2. Map Data: Specific Sunday Spikes
    sundays = df[
        (df["date"].apply(lambda x: x.weekday()) == 6) & (df["age_18_greater"] > 10)
    ].copy()
    sundays["type"] = "Sunday Shift"
    map_data = sundays[
        ["pincode", "district", "state", "age_18_greater", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- AGGREGATE MAP ENDPOINT ---
def get_all_map_anomalies(db: Session):
    """Combines map data from all 6 engines for the Main Panel"""
    # Note: In production, optimize this to avoid re-calculating everything.
    # For hackathon, calling functions sequentially is acceptable.

    phantom = analyze_phantom_village(db)["map_data"]
    update_mill = analyze_update_mill(db)["map_data"]
    bio_bypass = analyze_biometric_bypass(db)["map_data"]
    sunday = analyze_sunday_shift(db)["map_data"]

    # Add coordinates (MOCKING LAT/LNG based on Pincode for Visualization)
    # Since real geocoding requires external APIs not allowed or rate-limited.
    def mock_coords(pincode):
        # Deterministic pseudo-random lat/lng roughly within India

        random.seed(pincode)  # noqa: F821
        lat = 20 + (random.random() * 10)  # noqa: F821  # 20-30 Lat
        lng = 75 + (random.random() * 10)  # noqa: F821  # 75-85 Lng
        return lat, lng

    all_anomalies = phantom + update_mill + bio_bypass + sunday

    final_data = []
    for item in all_anomalies:
        lat, lng = mock_coords(item["pincode"])
        item["lat"] = lat
        item["lng"] = lng
        final_data.append(item)

    return final_data
