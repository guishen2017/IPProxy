#-*- coding:utf-8 -*-
from flask import Flask,g
from db import RedisClient

app = Flask(__name__)

def get_conn():
    if not hasattr(g, "db"):
        g.db = RedisClient()
    return g.db

@app.route("/")
def index():
    return "<h2>Welcome Come!!</h2>"

@app.route("/random/")
def random():
    db = get_conn()
    return db.random()

@app.route("/count/")
def count():
    db = get_conn()
    return str(db.count())
if __name__ == "__main__":
    app.run()
