#-*- coding:utf-8 -*-
import time
from multiprocessing import Process
from getter import Getter
from tester import Tester
import time
from api import app
from settings import *

class Scheduler():
    def schedule_tester(self, cycle = TEST_CYCLE_TIME):
        tester = Tester()
        while True:
            print("测试模块运行")
            tester.run()
            time.sleep(cycle)

    def schedule_crawl(self, cycle = CRAWL_CYCLE_TIME):
        crawl = Getter()
        while True:
            print("抓取模块运行")
            crawl.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run()

    def run(self):
        print("代理池开始运行")
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            crawler_process = Process(target=self.schedule_crawl)
            crawler_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == "__main__":
    schedule = Scheduler()
    schedule.run()