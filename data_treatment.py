import krakenex
import datetime

kraken = krakenex.API()

pair = 'XBTUSD'

interval = '1440'

response = kraken.query_public('OHLC', {'pair': pair, 'interval': interval})

if response['error']:
    print("Error occurred:", response['error'])
else:
    for i in response['result']['XXBTZUSD']:
        print(datetime.datetime.utcfromtimestamp(i[0]), i[1:])
