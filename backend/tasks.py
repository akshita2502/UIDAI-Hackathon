"""
Background Task Runner
Usage:
    python tasks.py phantom
    python tasks.py update
    python tasks.py map
    ...
    python tasks.py all  (Runs everything sequentially)
"""

import time
import argparse
from database import SessionLocal
import ai_engine
from redis_client import set_cached_data

# Cache Keys mapping
KEYS = {
    "map": "dashboard:map_data",
    "phantom": "dashboard:phantom_village",
    "update": "dashboard:update_mill",
    "bio": "dashboard:biometric_bypass",
    "ghost": "dashboard:scholarship_ghost",
    "bot": "dashboard:bot_operator",
    "sunday": "dashboard:sunday_shift",
}


def run_job(job_name, function, key):
    """Helper to run a single job with DB session management"""
    print(f"[{job_name.upper()}] Starting computation...")
    start_time = time.time()

    db = SessionLocal()
    try:
        # Run the AI Engine analysis
        result = function(db)

        # Extract data: 'map' job returns list directly, others return dict with 'chart_data'
        data_to_cache = result if job_name == "map" else result.get("chart_data")

        if data_to_cache:
            set_cached_data(key, data_to_cache)
            elapsed = time.time() - start_time
            print(f"[{job_name.upper()}] ✓ Completed & Cached in {elapsed:.2f}s")
        else:
            print(f"[{job_name.upper()}] ⚠ No data returned.")

    except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
        print(f"[{job_name.upper()}] ✗ Failed: {str(e)}")
    finally:
        db.close()


# --- Individual Job Wrappers ---


def task_phantom():
    """Run Phantom Village Analysis Task"""
    run_job("phantom", ai_engine.analyze_phantom_village, KEYS["phantom"])


def task_update():
    """Run Update Mill Analysis Task"""
    run_job("update", ai_engine.analyze_update_mill, KEYS["update"])


def task_bio():
    """Run Biometric Bypass Analysis Task"""
    run_job("bio", ai_engine.analyze_biometric_bypass, KEYS["bio"])


def task_ghost():
    """Run Scholarship Ghost Analysis Task"""
    run_job("ghost", ai_engine.analyze_scholarship_ghost, KEYS["ghost"])


def task_bot():
    """Run Bot Operator Analysis Task"""
    run_job("bot", ai_engine.analyze_bot_operator, KEYS["bot"])


def task_sunday():
    """Run Sunday Shift Analysis Task"""
    run_job("sunday", ai_engine.analyze_sunday_shift, KEYS["sunday"])


def task_map():
    """Run Map Anomalies Aggregation Task"""
    # Note: This is the heaviest task as it aggregates multiple models
    run_job("map", ai_engine.get_all_map_anomalies, KEYS["map"])


def run_all():
    """Run all analysis tasks sequentially"""
    task_phantom()
    task_update()
    task_bio()
    task_ghost()
    task_bot()
    task_sunday()
    task_map()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific background tasks.")
    parser.add_argument(
        "job",
        nargs="?",
        default="all",
        choices=["all", "phantom", "update", "bio", "ghost", "bot", "sunday", "map"],
        help="The specific analytics job to run.",
    )

    args = parser.parse_args()

    job_map = {
        "phantom": task_phantom,
        "update": task_update,
        "bio": task_bio,
        "ghost": task_ghost,
        "bot": task_bot,
        "sunday": task_sunday,
        "map": task_map,
        "all": run_all,
    }

    if args.job in job_map:
        job_map[args.job]()
    else:
        print("Invalid job name.")
