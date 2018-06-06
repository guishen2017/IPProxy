#-*- coding:utf-8 -*-
from settings import *
import redis
from random import choice
from pool_exception import PoolExcetion

class RedisClient(object):
    def __init__(self, host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self,proxy,score=DEFAULT_SCORE):
        return self.db.zadd(REDIS_KEY, score, proxy)

    def max(self, proxy, socre = MAX_SCORE):
        return self.db.zadd(REDIS_KEY, socre, proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrangebyscore(REDIS_KEY,MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolExcetion
    def all(self):
        return self.db.zrevrangebyscore(REDIS_KEY, MAX_SCORE,MIN_SCORE)

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print(proxy,"分数是",score,"减1")
            self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print(proxy, "分数是0,移除")
            self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        return self.db.zscore(REDIS_KEY, proxy) != None

    def batch(self, start, stop):
        return self.db.zrange(REDIS_KEY, start, stop-1)

if __name__ =="__main__":
    db = RedisClient()
    print(db.count())
    # print(db.all())
    # print(db.add("93.17.7.146:82"))
    # print(db.exists("93.17.7.146:80"))






