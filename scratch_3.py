# Description: This script connects to the Alpaca Market API via a WebSocket
import json
import websocket
import asyncio

# Replace these with your Alpaca API key and secret
SEC_KEY = 'erU539BdUUsStoJCLuJANSgI6cI8TEYj9gcZbpRd'  # Enter Your Secret Key Here
PUB_KEY = 'PKZBJS2I4QCXLGEI9V5T'  # Enter Your Public Key Here

# Define the URL for the Alpaca Market API
url = "wss://testnet-explorer.binance.org/ws/block"

# Define the authentication message
auth_message = {
    "action": "auth",
    "key": PUB_KEY,
    "secret": SEC_KEY
}


def on_open(ws):
    print("Connection Opened")


def on_message(ws, message):
    print(message)


def on_close(ws, error):
    print("Connection Closed")
    print(error)


ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message)

ws.run_forever()