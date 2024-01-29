from . import settings 

from redis import Redis, ConnectionPool


pool = ConnectionPool.from_url(url= settings.REDIS_URL,max_connections=100)

class RedisConfig:

    def __init__(self):
        self.redis = Redis(connection_pool=pool)

