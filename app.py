from flask import Flask, Response
import requests
import json
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"





if __name__ == '__main__':
    app.run()
