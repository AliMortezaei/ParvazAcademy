from types import NoneType
from typing import Any
from django.utils.timezone import datetime, timedelta


from core.redis_config import RedisConfig
from redis.exceptions import RedisError
from .exception import ServiceUnavailableException, NotFoundException


class RedisManager(RedisConfig):



    def get_by_redis(self, key: str) -> Any:
        try:
            data = self.redis.get(key)

            return self.deserialize(data.decode())
        except RedisError as exp:
            raise ServiceUnavailableException()
        except (TypeError, ValueError, AttributeError):
            raise NotFoundException()

        


    def add_to_redis(self, code, **kwargs) -> bool:
        try:
            key = self.serialize(
                code= code, email= kwargs['email'],
                full_name= kwargs['full_name'], password= kwargs['password']
            )

            self.redis.set(str(kwargs['phone_number']), str(key), ex=timedelta(minutes=30))    
            return kwargs['phone_number']
        except RedisError as exp:
            raise ServiceUnavailableException()
        
    def serialize(self, code, full_name, email, password):
        return f'{code},{full_name},{email},{password}'

    def deserialize(
        self,
        value: str,
        key: list = ['code', 'full_name', 'email', 'password']
    ):
        values = value.split(',')
        result = zip(key, values)
        return dict(result)

