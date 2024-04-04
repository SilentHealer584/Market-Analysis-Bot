import krakenex
import datetime
import numpy as np

def calculate_ema(data, window):
    close_prices = [float(entry[4]) for entry in data]
    ema = []
    for i in range(len(close_prices)):
        if i < window:
            ema.append(None)  # EMA not available until there are enough data points
        else:
            ema.append(np.mean(close_prices[i - window:i]))
    return ema

kraken = krakenex.API()

pair = 'XBTUSD'
interval = '1440'

response = kraken.query_public('OHLC', {'pair': pair, 'interval': interval})

if response['error']:
    print("Error occurred:", response['error'])
else:
    data = response['result']['XXBTZUSD'][-90:]
    ema_9 = calculate_ema(data, 9)
    for i in range(len(data)):
        print(datetime.datetime.utcfromtimestamp(data[i][0]), "EMA_9:", ema_9[i])
