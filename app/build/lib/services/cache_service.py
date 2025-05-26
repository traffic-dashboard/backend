import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def get_cached_value(key: str):
    return redis_client.get(key)

def set_cached_value(key: str, value, ttl: int = 300):
    redis_client.setex(key, ttl, value)
