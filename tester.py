#-*- coding:utf-8 -*-
import time
from db import RedisClient
import asyncio
import aiohttp
from settings import *

class Tester(object):
    def __init__(self):
        self.db = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = "http://"+proxy
                async with session.get(url=TEST_URL, proxy=real_proxy, timeout = 15, allow_redirects=False) as response:
                    if response.status in VALUE_CODE:
                        print("代理",proxy,"有效,分数置为100")
                        self.db.max(proxy)
                    else:
                        print("代理",proxy,"响应码，分数减1")
                        self.db.decrease(proxy)
            except Exception:
                print("代理", proxy, "请求出错,分数减1")
                self.db.decrease(proxy)

    def run(self):
        count = self.db.count()
        print('当前剩余', count, '个代理')
        for i in range(0,count, BATCH):
            start = i
            end = min(i+BATCH,count)
            proxies = self.db.batch(start, end)
            print('正在测试第', start + 1, '-', end, '个代理')
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in proxies]
            loop.run_until_complete(asyncio.wait(tasks))
            time.sleep(5)

if __name__ == "__main__":
    test = Tester()
    test.run()
