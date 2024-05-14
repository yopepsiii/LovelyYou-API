import redis


class RedisTools:
    __redis_connect = redis.Redis(host="redis", port=6379)

    @classmethod
    def set_pair(cls, pair_key: str, pair_value):
        cls.__redis_connect.set(pair_key, pair_value)

    @classmethod
    def get_pair(cls, pair_key: str):
        return cls.__redis_connect.get(pair_key)

    @classmethod
    def get_keys(cls):
        return cls.__redis_connect.keys(pattern="*")
