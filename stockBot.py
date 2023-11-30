# This is the code for Greg's stock bot functions. This is the code that is used to manage the stock account

import alpaca.trading as tradeAPI
import numpy as np

# The secret key and public key for my paper stock account
SEC_KEY = 'erU539BdUUsStoJCLuJANSgI6cI8TEYj9gcZbpRd'  # Enter Your Secret Key Here
PUB_KEY = 'PKZBJS2I4QCXLGEI9V5T'  # Enter Your Public Key Here
BASE_URL = 'https://paper-api.alpaca.markets'  # This is the base URL for paper trading
api = tradeAPI.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)  # For real trading, don't enter a base_url


def getAccount():
    # This function will return the account information
    return api.get_account()


def getPosition(ticker):
    # This function will return the position of the stock
    # ticker is the ticker of the stock
    try:
        return api.get_position(ticker)
    except:  # If the stock is not in the portfolio, return 0
        return 0


def manageStock(ticker, order):
    # This function will manage the stock account
    # ticker is the ticker of the stock
    # order is the order to be placed

    if order == "buy" or order == "sell":
        api.submit_order(
            symbol=ticker,
            qty=1,
            side=order,
            type='market',
            time_in_force='gtc')

    else:
        return 0


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
