"""AI engine module for UIDAI Sentinel fraud detection algorithms"""

from concurrent.futures import ThreadPoolExecutor
import random
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
import models

# --- STATE NORMALIZATION MAPPING ---
# Maps various state name variations to a standardized format
STATE_NORMALIZATION = {
    # Variations -> Standard Name
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    # Merging Daman, Diu, Dadra, Nagar Haveli
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "the dadra and nagar haveli and daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli and daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "lakshadweep": "Lakshadweep",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal",
    "westbengal": "West Bengal",
    "west bangal": "West Bengal",
}
# --- GEOSPATIAL CONFIGURATION ---

# 1. PRECISE DISTRICT COORDINATES (Prioritize these for accuracy)
DISTRICT_COORDS = {
    # Karnataka
    "Bengaluru Urban": [12.9716, 77.5946],
    "Bengaluru Rural": [13.2847, 77.5712],
    "Mysuru": [12.2958, 76.6394],
    "Dakshina Kannada": [12.9141, 74.8560],
    # Maharashtra
    "Pune": [18.5204, 73.8567],
    "Mumbai": [19.0760, 72.8777],
    "Mumbai Suburban": [19.1828, 72.8523],
    "Thane": [19.2183, 72.9781],
    "Nagpur": [21.1458, 79.0882],
    "Nashik": [19.9975, 73.7898],
    # Tamil Nadu
    "Chennai": [13.0827, 80.2707],
    "Coimbatore": [11.0168, 76.9558],
    "Madurai": [9.9252, 78.1198],
    "Kancheepuram": [12.8185, 79.6947],
    # Telangana & AP
    "Hyderabad": [17.3850, 78.4867],
    "Ranga Reddy": [17.4399, 78.4983],
    "Visakhapatnam": [17.6868, 83.2185],
    "Krishna": [16.5062, 80.6480],
    # North India
    "New Delhi": [28.6139, 77.2090],
    "Central Delhi": [28.6465, 77.2410],
    "Gurugram": [28.4595, 77.0266],
    "Gautam Buddha Nagar": [28.5355, 77.3910],  # Noida
    "Lucknow": [26.8467, 80.9462],
    "Jaipur": [26.9124, 75.7873],
    "Chandigarh": [30.7333, 76.7794],
    # East/North-East
    "Kolkata": [22.5726, 88.3639],
    "Patna": [25.5941, 85.1376],
    "Guwahati": [26.1158, 91.7086],
    "East Khasi Hills": [25.5788, 91.8933],  # Shillong
}

# 2. STATE FALLBACKS (Used if District is missing)
STATE_COORDS = {
    "Tamil Nadu": [11.1271, 78.6569],
    "Karnataka": [15.3173, 75.7139],
    "Maharashtra": [19.7515, 75.7139],
    "Uttar Pradesh": [26.8467, 80.9462],
    "Meghalaya": [25.4670, 91.3662],
    "Bihar": [25.0961, 85.3131],
    "West Bengal": [22.9868, 87.8550],
    "Andhra Pradesh": [15.9129, 79.7400],
    "Telangana": [18.1124, 79.0193],
    "Rajasthan": [27.0238, 74.2179],
    "Gujarat": [22.2587, 71.1924],
    "Haryana": [29.0588, 76.0856],
    "Odisha": [20.9517, 85.0985],
    "Jammu and Kashmir": [33.2778, 75.3412],
    "Kerala": [10.8505, 76.2711],
    "Assam": [26.2006, 92.9376],
    "Punjab": [31.1471, 75.3412],
    "Chhattisgarh": [21.2787, 81.8661],
    "Madhya Pradesh": [22.9734, 78.6569],
    "Jharkhand": [23.6102, 85.2799],
    "Uttarakhand": [30.0668, 79.0193],
    "Himachal Pradesh": [31.1048, 77.1734],
    "Tripura": [23.9408, 91.9882],
    "Mizoram": [23.1645, 92.9376],
    "Manipur": [24.6637, 93.9063],
    "Nagaland": [26.1584, 94.5624],
    "Goa": [15.2993, 74.1240],
    "Arunachal Pradesh": [28.2180, 94.7278],
    "Sikkim": [27.5330, 88.5122],
    "Delhi": [28.7041, 77.1025],
}


def get_coords(state, district, pincode):
    """
    Returns high-precision coordinates.
    Priority: District Match > State Match > India Center
    """
    spread = 0.5  # Default wide spread

    # 1. Try Accurate District Match
    if district and district in DISTRICT_COORDS:
        base = DISTRICT_COORDS[district]
        spread = 0.05  # Very tight spread (~5km) for accuracy
    # 2. Fallback to State Match
    elif state and state in STATE_COORDS:
        base = STATE_COORDS[state]
        spread = 0.5  # Wider spread (~50km)
    # 3. Default Fallback
    else:
        base = [22.9734, 78.6569]
        spread = 2.0

    # Deterministic Jitter using Pincode
    if pincode:
        np.random.seed(int(pincode))
    else:
        np.random.seed(42)

    lat_offset = (np.random.rand() - 0.5) * spread
    lng_offset = (np.random.rand() - 0.5) * spread

    return base[0] + lat_offset, base[1] + lng_offset


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
    Detects Phantom Village anomalies and Returns CLEANED State-wise data.
    """
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    # 1. Isolation Forest Logic
    model = IsolationForest(contamination=0.01, random_state=42)
    df["anomaly"] = model.fit_predict(df[["age_18_greater"]].fillna(0))

    # 2. Data Cleaning & Normalization
    # Convert state column to string, strip whitespace, and lower case for matching
    df["state_clean"] = df["state"].astype(str).str.strip().str.lower()

    # Map to standard names using the dictionary
    df["normalized_state"] = df["state_clean"].map(STATE_NORMALIZATION)

    # Fill unknown/numeric states (like "10000") with "Others" or drop them
    # For this chart, we usually drop "Others" to keep it to 28+8
    df = df.dropna(subset=["normalized_state"])

    # 3. Aggregation on NORMALIZED State
    state_stats = (
        df.groupby(["normalized_state", "anomaly"]).size().unstack(fill_value=0)
    )

    # Rename columns: -1 is Anomaly, 1 is Normal
    if -1 in state_stats.columns:
        state_stats = state_stats.rename(
            columns={-1: "anomaly_count", 1: "normal_count"}
        )
    else:
        state_stats["anomaly_count"] = 0
        state_stats = state_stats.rename(columns={1: "normal_count"})

    # 4. Final Formatting
    chart_data = state_stats.reset_index().rename(columns={"normalized_state": "state"})

    # Sort alphabetically for consistent X-Axis
    chart_data = chart_data.sort_values("state")

    return {
        "chart_data": chart_data.to_dict(orient="records"),
        # Map data logic remains the same (using raw names is fine for coordinates lookup)
        "map_data": (
            df[df["anomaly"] == -1][
                ["pincode", "district", "state", "age_18_greater", "type"]
            ].to_dict(orient="records")
            if "type" in df.columns
            else []
        ),
    }


# --- 2. UPDATE MILL (Unauthorized Bulk Ops) ---
def analyze_update_mill(db: Session):
    """Detects Update Mill (Unauthorized Bulk Operations)."""
    df = get_dataframe(db, models.DemographicData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    # Z-Score
    stats = df.groupby("district")["demo_age_17_"].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    df["z_score"] = stats.fillna(0)

    # Chart Data
    top_districts = (
        df[["district", "z_score"]]
        .drop_duplicates()
        .sort_values("z_score", ascending=False)
        .head(20)
    )
    chart_data = top_districts.to_dict(orient="records")

    # Map Data - RELAXED THRESHOLD: Z-Score > 2 (was 3)
    suspects = df[df["z_score"] > 2].copy()
    suspects["type"] = "Update Mill"
    map_data = suspects[
        ["pincode", "district", "state", "z_score", "demo_age_17_", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 3. BIOMETRIC BYPASS (Incomplete Verification) ---
def analyze_biometric_bypass(db: Session):
    """Detects Biometric Bypass (Incomplete Verification)."""
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty:
        return {"chart_data": [], "map_data": []}

    merged = pd.merge(demo_df, bio_df, on=["date", "state", "district", "pincode"])

    # Risk Score
    merged["risk_score"] = merged["demo_age_17_"] / (merged["bio_age_17_"] + 1)

    # Chart Data
    chart_data = (
        merged[["demo_age_17_", "bio_age_17_", "risk_score"]]
        .sample(min(200, len(merged)))
        .to_dict(orient="records")
    )

    # Map Data - RELAXED THRESHOLD: Risk > 1.5 (was 5)
    # This means Demographic updates are just 1.5x of Biometric updates
    high_risk = merged[merged["risk_score"] > 1.5].copy()
    high_risk["type"] = "Biometric Bypass"
    map_data = high_risk[
        ["pincode", "district", "state", "risk_score", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 4. SCHOLARSHIP GHOST (Child Age/Bio Mismatch) ---
def analyze_scholarship_ghost(db: Session):
    """Detects Scholarship Ghost (Child Age/Bio Mismatch)."""
    demo_df = get_dataframe(db, models.DemographicData)
    bio_df = get_dataframe(db, models.BiometricData)
    if demo_df.empty or bio_df.empty:
        return {"chart_data": [], "map_data": []}

    merged = pd.merge(demo_df, bio_df, on=["date", "state", "district", "pincode"])

    # Group stats
    district_stats = (
        merged.groupby("district")[["demo_age_5_17", "bio_age_5_17"]]
        .sum()
        .reset_index()
    )
    district_stats["mismatch_ratio"] = district_stats["demo_age_5_17"] / (
        district_stats["bio_age_5_17"] + 1
    )
    chart_data = (
        district_stats.sort_values("mismatch_ratio", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

    # Map Data - RELAXED THRESHOLD
    # Demo > 10 (was 20) AND Bio < 5
    suspects = merged[
        (merged["demo_age_5_17"] > 10) & (merged["bio_age_5_17"] < 5)
    ].copy()
    suspects["type"] = "Scholarship Ghost"

    if len(suspects) > 200:
        suspects = suspects.head(200)

    map_data = suspects[
        ["pincode", "district", "state", "demo_age_5_17", "bio_age_5_17", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- 5. BOT OPERATOR (Benford's Law) ---
def analyze_bot_operator(db: Session):
    """Detects Bot Operator (Round Numbers)."""
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

    # Chart Data
    suspicious_count = len(pincode_stats[pincode_stats["round_pct"] > 80])
    natural_count = len(pincode_stats) - suspicious_count
    chart_data = [
        {"name": "Suspicious (>80% Round)", "value": suspicious_count},
        {"name": "Natural", "value": natural_count},
    ]

    # Map Data
    bots = pincode_stats[pincode_stats["round_pct"] > 80].copy()
    bots["type"] = "Bot Operator"

    # Merge back state/district info (using first occurrence)
    meta_df = df[["pincode", "state", "district"]].drop_duplicates("pincode")
    bots = pd.merge(bots, meta_df, on="pincode", how="left")

    map_data = bots[["pincode", "district", "state", "type", "round_pct"]].to_dict(
        orient="records"
    )

    return {"chart_data": chart_data, "map_data": map_data}


# --- 6. SUNDAY SHIFT (Temporal Anomaly) ---
def analyze_sunday_shift(db: Session):
    """Detects Sunday Shift (Temporal Anomaly)."""
    df = get_dataframe(db, models.EnrolmentData)
    if df.empty:
        return {"chart_data": [], "map_data": []}

    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].apply(lambda x: x.strftime("%A"))

    # Chart Data
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

    # Map Data - RELAXED THRESHOLD: > 5 (was 10)
    sundays = df[
        (df["date"].apply(lambda x: x.weekday()) == 6) & (df["age_18_greater"] > 5)
    ].copy()
    sundays["type"] = "Sunday Shift"
    map_data = sundays[
        ["pincode", "district", "state", "age_18_greater", "type"]
    ].to_dict(orient="records")

    return {"chart_data": chart_data, "map_data": map_data}


# --- AGGREGATE MAP ENDPOINT ---
def get_all_map_anomalies(db: Session):
    """
    Combines map data from all 6 engines.
    Uses ThreadPoolExecutor for parallel execution.
    """
    with ThreadPoolExecutor(max_workers=6) as executor:
        phantom_future = executor.submit(analyze_phantom_village, db)
        update_future = executor.submit(analyze_update_mill, db)
        bio_future = executor.submit(analyze_biometric_bypass, db)
        ghost_future = executor.submit(analyze_scholarship_ghost, db)
        bot_future = executor.submit(analyze_bot_operator, db)
        sunday_future = executor.submit(analyze_sunday_shift, db)

        # Collect results
        phantom = phantom_future.result().get("map_data", [])
        update_mill = update_future.result().get("map_data", [])
        bio_bypass = bio_future.result().get("map_data", [])
        ghost = ghost_future.result().get("map_data", [])
        bot = bot_future.result().get("map_data", [])
        sunday = sunday_future.result().get("map_data", [])

    all_anomalies = phantom + update_mill + bio_bypass + ghost + bot + sunday

    # Limit for UI performance
    if len(all_anomalies) > 1000:
        # Simple sampling to ensure variety
        random.shuffle(all_anomalies)
        all_anomalies = all_anomalies[:1000]

    final_data = []
    for item in all_anomalies:
        # Use refined get_coords with District priority
        lat, lng = get_coords(
            item.get("state"), item.get("district"), item.get("pincode")
        )
        item["lat"] = lat
        item["lng"] = lng
        final_data.append(item)

    return final_data
