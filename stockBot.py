# This is the code for Greg's stock bot functions. This is the code that is used to manage the stock account

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
import numpy as np
import websockets
import json
import ast
import time
import asyncio
from tqdm import tqdm

# The global variables everything else needs
SEC_KEY = 'erU539BdUUsStoJCLuJANSgI6cI8TEYj9gcZbpRd'  # Enter Your Secret Key Here
PUB_KEY = 'PKZBJS2I4QCXLGEI9V5T'  # Enter Your Public Key Here
BASE_URL = 'https://paper-api.alpaca.markets'  # This is the base URL for paper trading
client = TradingClient(PUB_KEY, secret_key=SEC_KEY, paper=True)  # This is the client object
account = dict(client.get_account())  # This is the account object


def stringToDictionary(string):
    newList = ast.literal_eval(string)
    return newList[0]


def getQuantity(ticker):
    # Get a list of all of our positions.
    portfolio = client.get_all_positions()
    # Print the quantity of shares for each position.
    for position in portfolio:
        qty, symbol = position.qty, position.symbol
        if symbol == ticker:
            return qty, position.avg_entry_price

    return 0, 0

def subscriptionMessage(ticker, unsubscribe=False):
    subscription = "subscribe" if not unsubscribe else "unsubscribe"
    return {"action": "subscribe",
            "trades": [ticker],
            "bars": [ticker]}


def manageStock(ticker, order, qty=1):
    # This function will manage the stock account
    # ticker is the ticker of the stock

    if order == "buy":
        orderDetails = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.BUY,
            type=OrderType.MARKET,
            time_in_force=TimeInForce.DAY
        )
    elif order == "sell":
        orderDetails = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            type=OrderType.MARKET,
            time_in_force=TimeInForce.DAY
        )
    else:
        return 0

    client.submit_order(order_data=orderDetails)


def closeEverything():
    client.close_all_positions()


# NOTE: This code can take multiple minutes to run
# It also returns two dictionaries, one for general data and one for bars data
async def getMarketData(ticker):
    url = "wss://stream.data.alpaca.markets/v2/iex"

    auth_message = {
        "action": "auth",
        "key": PUB_KEY,
        "secret": SEC_KEY
    }

    async with websockets.connect(url) as ws:
        # First, connect to the websocket
        if stringToDictionary(await ws.recv())["msg"] == "connected":
            await ws.send(json.dumps(auth_message))

            # Then, authenticate
            if stringToDictionary(await ws.recv())["msg"] == "authenticated":

                # Then, subscribe to the ticker
                await ws.send(json.dumps(subscriptionMessage(ticker)))
                await ws.recv()

                # Now just wait for something to come in and return it
                while True:
                    hasBars = False
                    hasGeneral = False
                    general = []
                    bars = []

                    while not hasBars or not hasGeneral:
                        message = await ws.recv()
                        tempMessage = stringToDictionary(message)
                        if tempMessage["T"] == "b":
                            hasBars = True
                            bars = message
                        elif tempMessage["T"] == "t":
                            hasGeneral = True
                            general = message

                    generalDict = stringToDictionary(general)
                    barsDict = stringToDictionary(bars)

                    return generalDict, barsDict


async def mainLogic(ticker):
    marketData, marketBars = await getMarketData(ticker)
    quantity, purchasePrice = getQuantity(ticker)  # This will return 0 if the stock is not in the portfolio

    print(quantity, purchasePrice)

    positionHeld = True if quantity != 0 else False

    print(positionHeld)

    closeList = [marketBars["c"]]  # This array will store all the closing prices from the last 5 minutes

    for i in tqdm(range(4)):
        marketData, newBars = await getMarketData(ticker)
        closeList.append(newBars["c"])

    print(closeList)

    closeList = np.array(closeList, dtype=np.float64)  # Convert to numpy array
    ma = np.mean(closeList)
    lastPrice = marketData['p']  # Most recent closing price

    if ma + 0.1 < lastPrice and not positionHeld:  # If MA is more than 10cents under price, and we haven't bought
        return "buy"
    elif ma - 0.1 > lastPrice and positionHeld:  # If MA is more than 10cents above price, and we already bought
        return "sell"
    else:
        return "hold"


def mainProgram(stocks):
    for ticker in stocks:
        manageStock(ticker, asyncio.run(mainLogic("SPY")), int(getQuantity(ticker)[0]))


# price, bars = asyncio.run(getMarketData("AAPL"))
# print(price,bars)
#
# print(account)
#
# Get our position in AAPL.
# aapl_position = client.get_open_position('AAPL').avg_entry_price # This tells us how much we paid for something

print(asyncio.run(mainLogic("AAPL")))