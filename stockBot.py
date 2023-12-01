# This is the code for Greg's stock bot functions. This is the code that is used to manage the stock account

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import numpy as np

# The global variables everything else needs
SEC_KEY = 'erU539BdUUsStoJCLuJANSgI6cI8TEYj9gcZbpRd'  # Enter Your Secret Key Here
PUB_KEY = 'PKZBJS2I4QCXLGEI9V5T'  # Enter Your Public Key Here
BASE_URL = 'https://paper-api.alpaca.markets'  # This is the base URL for paper trading
client = TradingClient(key_id=PUB_KEY, secret_key=SEC_KEY, paper=True)  # This is the client object
account = dict(client.get_account())  #This is the account object


def getAccountData():
    # This funtion will return the account data
    assets = [i for i in client.get_all_positions]
    positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]
    return positions


def getPosition(ticker):
    # This function will return the position of the stock
    # ticker is the ticker of the stock
    positions = getAccountData()
    for position in positions:
        if position[0] == ticker:
            return position[1]

    return 0


def manageStock(ticker, order):
    # This function will manage the stock account
    # ticker is the ticker of the stock

    if order == "hold":
        return
    elif order == "buy":
        orderDetails = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=OrderSide.BUY,
            type=OrderType.MARKET,
        )
    elif order == "sell":
        orderDetails = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=OrderSide.SELL,
            type=OrderType.MARKET,
        )

    client.submit_order(order_data=orderDetails)


def closeEverything():
    client.close_all_positions()

def getMarketData(ticker):
    # This function will return the market data of the stock
    # ticker is the ticker of the stock
    return api.get_barset(ticker, 'minute', limit=5)


def mainLogic(ticker):
    market_data = getMarketData(ticker)
    pos_held = getPosition(
        ticker)  # This will return 0 if the stock is not in the portfolio, else it will return the position

    close_list = []  # This array will store all the closing prices from the last 5 minutes
    for bar in market_data[ticker]:
        close_list.append(bar.c)  # bar.c is the closing price of that bar's time interval

    close_list = np.array(close_list, dtype=np.float64)  # Convert to numpy array
    ma = np.mean(close_list)
    last_price = close_list[4]  # Most recent closing price

    if ma + 0.1 < last_price and not pos_held:  # If MA is more than 10cents under price, and we haven't already bought
        return "buy"
    elif ma - 0.1 > last_price and pos_held:  # If MA is more than 10cents above price, and we already bought
        return "sell"
    else:
        return "hold"


def mainProgram():
    manageStock("SPY", mainLogic("SPY"))


mainProgram()
