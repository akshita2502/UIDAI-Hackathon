"""
Script to verify Redis connection and list cached dashboard keys.
Usage: python check_redis.py
"""

import os
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HOST = os.getenv("REDIS_HOST") or "localhost"
PORT = int(os.getenv("REDIS_PORT") or "6380")
DB = int(os.getenv("REDIS_DB") or "0")

print(f"🔌 Connecting to Redis at {HOST}:{PORT} (DB: {DB})...")

try:
    # Connect
    r = redis.Redis(host=HOST, port=PORT, db=DB, decode_responses=True)
    r.ping()
    print("✅ Connection Successful!")

    # Check Keys
    print("\n🔎 Scanning for Dashboard Keys...")
    keys_response = r.keys("dashboard:*")
    # Type assertion for sync client - keys should be a list
    keys = keys_response if isinstance(keys_response, list) else list(keys_response)  # type: ignore

    if not keys:
        print("❌ No 'dashboard:*' keys found. The cache is EMPTY.")
        print("   -> Run 'python tasks.py all' to populate the cache.")
    else:
        print(f"✅ Found {len(keys)} cached items:")
        print("-" * 50)
        print(f"{'KEY':<30} | {'TTL (sec)':<10} | {'SIZE (chars)':<10}")
        print("-" * 50)
        for key in keys:
            ttl = r.ttl(key)
            val = r.get(key)
            SIZE = len(str(val)) if val else 0
            print(f"{key:<30} | {ttl:<10} | {SIZE:<10}")
        print("-" * 50)

except redis.ConnectionError as e:
    print(f"❌ Connection Failed: {e}")
    print("   -> Check if Docker container is running: 'docker ps'")
    print("   -> Check port mapping in docker-compose.yaml")
