from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import time
import os

os.system("cls")

symbol = str(input("ticker: "))
contract_size = float(input("# of shares: "))

api_key = 'YOUR_API_KEY_HERE'
api_secret = 'YOUR_API_SECRET_HERE'

client = Client(api_key, api_secret)

doge = TA_Handler(
    symbol=f"{symbol}",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

def market_buy(symbol, contract_size):
    try:
        market_buy = client.futures_create_order(
        symbol = symbol,
        side = Client.SIDE_BUY,
        type = Client.ORDER_TYPE_MARKET,
        quantity = contract_size)

    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:
        print(e)

def market_sell(symbol, contract_size):
    try:
        market_sell = client.futures_create_order(
        symbol = symbol,
        side = Client.SIDE_SELL,
        type = Client.ORDER_TYPE_MARKET,
        quantity = contract_size)

    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:
        print(e)

last_recommendation = None

while True:
    recommendation = doge.get_analysis().summary
    if isinstance(recommendation, dict):
        recommendation = recommendation.get('RECOMMENDATION')
    if last_recommendation != recommendation:
        if recommendation == "STRONG_BUY":
            print("Buy signal recieved...")
            print("Validating purchase...")
            market_buy(symbol, contract_size)
            print("Purchase was completed successfully!")

        elif recommendation == "STRONG_SELL":
            print("Sell signal recieved...")
            print("Validating sale...")
            market_sell(symbol, contract_size)
            print("Sale was completed successfully!")
    time.sleep(0.5)

    last_recommendation = recommendation
    time.sleep(60) # wait for 60 seconds before checking for new recommendation