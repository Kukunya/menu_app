import redis
from menu_app.core.config import REDIS_URI


r = redis.Redis(host=REDIS_URI)
