import config
from binance.client import Client
from binance.enums import *

client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET, tld='us')

# getOrderHistory = client.get_all_orders()

# Exchange Variables
exchangeInfo = client.get_exchange_info()
exchangeSymbols = exchangeInfo['symbols']

# BTC Info
btcExchangeInfo = client.get_exchange_info()['symbols'][0]
btcTickerPrice = client.get_symbol_ticker()[0]['price']

# btcTest = client.get_symbol_ticker()[0]['price']

for i in exchangeSymbols:
    print(i)
    print("")
