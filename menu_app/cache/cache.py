import redis.asyncio as redis

# from menu_app.core.config import REDIS_URI

r: redis.Redis = redis.Redis()  # noqa
