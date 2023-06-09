# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : main.py                 #
# ----------------------------------------------- #

import json
import time
from waitress import serve
from flask import Flask, request

import config
from handler import *

app = Flask(__name__)


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp


@app.route("/webhook", methods=["POST"])
def resp():
    try:
        if request.method == "POST":
            data = request.get_json()
            key = data["key"]
            if key == config.sec_key:
                print(get_timestamp(), "Alert Received & Sent!")
                job(data)
                send_alert(data)
                return "OK", 200

            else:
                print("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Key)")
                return "Refused alert", 400

    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400

# @app.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         if request.method == "POST":
#             data = request.get_json()
#             key = data["key"]
#             if key == config.sec_key:
#                 print(get_timestamp(), "Alert Received & Sent!")
#                 send_alert(data)
#                 return "Sent alert", 200

#             else:
#                 print("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Key)")
#                 return "Refused alert", 400

#     except Exception as e:
#         print("[X]", get_timestamp(), "Error:\n>", e)
#         return "Error", 400



if __name__ == "__main__":
    print("Serving at http://localhost:80")
    init_mt5()
    serve(app, host="37.27.18.63", port=80)
