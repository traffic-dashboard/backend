import redis
import os
import redis.exceptions

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def get_cached_value(key: str):
    try:
        return redis_client.get(key)
    except redis.exceptions.ConnectionError:
        return None

def set_cached_value(key: str, value, ttl: int = 300):
    try:
        return redis_client.setex(key, ttl, value)
    except redis.exceptions.ConnectionError:
        return False
