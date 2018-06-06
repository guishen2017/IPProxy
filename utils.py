#-*- coding:utf-8 -*-
import requests

def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    }
    response = requests.get(url, headers=headers, allow_redirects = False)
    if response.status_code != 200:
        return None
    else:
        return response.text
