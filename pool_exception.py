#-*- coding:utf-8 -*-

class PoolExcetion(Exception):
    def __init__(self):
        super(PoolExcetion, self).__init__()

    def __str__(self):
        return "pool池枯竭"
