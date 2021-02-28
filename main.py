import config
from time import time, sleep
import json
import time
import binance_info
from sanic import Sanic
from sanic import response
from sanic.request import Request
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from binance.client import Client
from binance.enums import *

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="main")

myTime = int(time.time() * 1000)
trendFlag = False

client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET, tld='us')


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET, recvWindow=100000):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)

    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


def determineTrend(trend):
    print("determing trend:")
    global trendFlag
    if (trend == "uptrend"):
        trendFlag = True
        print("uptrend")
    elif (trend == "downtrend"):
        trendFlag = False
        print("downtrend")
    else:
        trendFlag = trendFlag
        if(trendFlag == True):
            print("uptrend")
        else:
            print("downtrend")


@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    data = request.json

    trend = data["strategy"]["flag"]

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:

        determineTrend(trend)

        if (trendFlag == False):
            return json({
                "code": "downtrend, waiting"
            })
        else:
            side = data['strategy']['order_action'].upper()
            quantity = data['strategy']['order_contracts']
            ticker = data['ticker']
            order_response = order(side, quantity, "DOGEUSD")

            if order_response:
                return json({
                    "code": "success",
                    "message": "order executed"
                })
            else:
                print("order failed")
                return json({
                    "code": "error",
                    "message": "order failed"
                })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
