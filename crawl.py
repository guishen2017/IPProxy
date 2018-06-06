#-*- coding:utf-8 -*-
from utils import get_page
from pyquery import PyQuery as pq

class CrawlMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__FUNC__'] = []
        count = 0
        for k,v in attrs.items():
            if "crawl_" in k:
                attrs['__FUNC__'].append(k)
                count += 1
        attrs['__FUNCOUNT'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=CrawlMetaClass):
    def get_proxies(self, fun_name):
        proxies = []
        for proxy in eval("self.{}()".format(fun_name)):
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=10):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    print("爬取到", ':'.join([ip, port]))
                    yield ':'.join([ip, port])

if __name__ == "__main__":
    crawler = Crawler()
    print(crawler.__FUNC__)


