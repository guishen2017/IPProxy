#-*- coding:utf-8 -*-
from db import RedisClient
from crawl import Crawler
from settings import *

class Getter(object):
    def __init__(self):
        self.db = RedisClient()
        self.crawl = Crawler()

    def is_over_threshold(self):
        if self.db.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        if not self.is_over_threshold():
            func_names = self.crawl.__FUNC__
            for func_name in func_names:
                proxies = self.crawl.get_proxies(func_name)
                for proxy in proxies:
                    self.db.add(proxy)

if __name__ =="__main__":
    getter = Getter()
    getter.run()
