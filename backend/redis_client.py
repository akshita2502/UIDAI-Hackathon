"""Redis client setup and utility functions"""

import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

# Connect to Redis
# Ensure Redis is running: docker run -p 6379:6379 -d redis
REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.getenv("REDIS_PORT") or "6379")
REDIS_DB = int(os.getenv("REDIS_DB") or "0")

try:
    REDIS_CLIENT = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,  # Automatically decode bytes to strings
    )
    # Quick connectivity check (optional, can be removed for prod)
    REDIS_CLIENT.ping()
except redis.ConnectionError as e:
    print(f"⚠ Warning: Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}: {e}")
    REDIS_CLIENT = None


def get_cached_data(key: str):
    """Retrieve JSON data from Redis"""
    if not REDIS_CLIENT:
        return None
    try:
        data = REDIS_CLIENT.get(key)
        return json.loads(data) if isinstance(data, str) else None
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error reading from Redis: {e}")
        return None


def set_cached_data(key: str, data: dict, expire_seconds: int = 604800):
    """Store dictionary as JSON in Redis with expiration (Default: 1 week)"""
    if REDIS_CLIENT:
        try:
            REDIS_CLIENT.setex(key, expire_seconds, json.dumps(data))
        except (redis.RedisError, json.JSONDecodeError, TypeError) as e:
            print(f"Error writing to Redis: {e}")
