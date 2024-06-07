import krakenex
import matplotlib.pyplot as plt
import pandas as pd
import ta

kraken = krakenex.API()

timeframe = 720

pair = 'XBTUSD'
interval = '240'

values = {'open': [],
          'close': [],
          'high': [],
          'low': []}

orders = {'buy': [[], []],
         'sell': [[], []]}

percentages = []

# Define plot's element's colors
bullish = '#ABABAB'
bearish = '#E0E0E0'
ema9_clr = '#D0F6D0'
ema21_clr = '#F6DAD0'
profit = buy_clr = '#4E9F42'
loss = sell_clr = '#E86666'

order_closed = True


# DEFINE YOUR INDICATORS (Ex: adx, rsi etc.)#


response = kraken.query_public('OHLC', {'pair': pair, 'interval': interval})

if response['error']:
    print("Error occurred:", response['error'])
else:
    data = response['result']['XXBTZUSD'][-timeframe:]

    # Prep Data for Plotting
    for y in data:
        values['open'].append(float(y[1]))
        values['high'].append(float(y[2]))
        values['low'].append(float(y[3]))
        values['close'].append(float(y[4]))

    # Convert lists to pandas Series
    values['open'] = pd.Series(values['open'])
    values['high'] = pd.Series(values['high'])
    values['low'] = pd.Series(values['low'])
    values['close'] = pd.Series(values['close'])
  

    for i in range(timeframe - 1):
        if #YOUR BUY CONDITIONS#:
            orders['buy'][0].append(i + 1)
            orders['buy'][1].append(values['open'][i + 1])
            order_closed = False

        elif #YOUR SELL CONDITIONS#:
            orders['sell'][0].append(i + 1)
            orders['sell'][1].append(values['open'][i + 1])
            order_closed = True
        
    if not order_closed:
        del orders['buy'][0][-1]
        del orders['buy'][1][-1]


    prices = pd.DataFrame(values)

    # Create figure for candlestick chart
    fig, ax = plt.subplots(figsize=(14, 8))

    # Define width of candlesticks
    width = 0.4
    width2 = 0.1

    up = prices[prices.close >= prices.open]
    down = prices[prices.close < prices.open]

    ax.bar(up.index, up.close - up.open, width, bottom=up.open, color=bullish)
    ax.bar(up.index, up.high - up.close, width2, bottom=up.close, color=bullish)
    ax.bar(up.index, up.low - up.open, width2, bottom=up.open, color=bullish)

    ax.bar(down.index, down.close - down.open, width, bottom=down.open, color=bearish)
    ax.bar(down.index, down.high - down.open, width2, bottom=down.open, color=bearish)
    ax.bar(down.index, down.low - down.close, width2, bottom=down.close, color=bearish)

    plt.xticks(rotation=45, ha='right')

    # DISPLAY INDICATORS (Using scatter as an example)
  
    # Display Buy/Sell Points
    ax.scatter(orders['buy'][0], orders['buy'][1], color=buy_clr, marker='v')

    for i, (x, y) in enumerate(zip(orders['buy'][0], orders['buy'][1])):
        ax.text(x, y + 600, 'BUY', ha='center', fontsize=6)

    ax.scatter(orders['sell'][0], orders['sell'][1], color=sell_clr, marker='v')

    for i, (x, y) in enumerate(zip(orders['sell'][0], orders['sell'][1])):
        ax.text(x, y + 600, 'SELL', ha='center', fontsize=6)

    # Display Orders
    for i in range(len(orders['buy'][0])):
        if orders['buy'][1][i] > orders['sell'][1][i]:
            ax.plot([orders['buy'][0][i], orders['sell'][0][i]], [orders['buy'][1][i], orders['sell'][1][i]],
                    color=loss)
        else:
            ax.plot([orders['buy'][0][i], orders['sell'][0][i]], [orders['buy'][1][i], orders['sell'][1][i]],
                    color=profit)

        mid_x = (orders['buy'][0][i] + orders['sell'][0][i]) / 2
        mid_y = (orders['buy'][1][i] + orders['sell'][1][i]) / 2
        change = (orders['sell'][1][i] / orders['buy'][1][i]) * 100 - 100

        percentages.append(change)

        ax.text(mid_x, mid_y, f'{change:.2f}%', ha='center', fontsize=8)

    plt.xlim(prices.index[-timeframe] - 1, prices.index[-1] + 3)

    print(len(percentages))

    equity = 100

    for i in percentages:
        equity = (equity * 0.75) + (equity * 0.25 * (1 + i / 100))

    print(equity)

    # Display candlestick chart
    plt.show()

    # Plot Equity curve
    equity_dates = range(len(percentages) + 1)
    equity_values = [100]  # Initial equity balance

    # Equity curve values calculation
    for i in range(len(percentages)):
        equity_values.append((equity_values[-1] * 0.75) + (equity_values[-1] * 0.25 * (1 + percentages[i] / 100)))

    average_pnl = (equity_values[-1] - 100)

    peak_value = equity_values[0]  # Initialize peak value
    max_drawdown = 0

    for value in equity_values:
        if value > peak_value:
            peak_value = value  # Update peak value if a new peak is encountered
        else:
            drawdown = (peak_value - value) / peak_value * 100  # Calculate drawdown from peak
            max_drawdown = max(max_drawdown, drawdown)  # Update maximum drawdown if current drawdown is greater

    print("MDD:", f'{max_drawdown:.2f}%')

    plt.figure(figsize=(10, 6))
    plt.plot(equity_dates, equity_values, linestyle='-')

    plt.xlabel('Trade Number')
    plt.ylabel('Equity Balance')

    plt.grid(True)
    plt.tight_layout()
    plt.show()
