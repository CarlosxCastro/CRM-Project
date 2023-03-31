'''
CC
Trading Bot

Must use BINANCE 
This code uses python and cctxt 
that builds a strategy to buy a
stock/BTC when price is over 20sma
then hold for at least 5 days. 
It will then sell when price drops
below 40sma. Use this at your own risk.
Honestly, I wouldn't use it since this is 
test code. 

'''

import dontshareconfig
import ccxt
import time
import pandas as pd

# initialize exchange object
# add api keys
exchange = ccxt.binance()

exchange = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': dontshareconfig.get('apiKey'),
    'secret': secret_key,
})

def bot():

# set up parameters
symbol = 'AAPL/USDT'
#timeframe = '1d'
#sma_period = 20
#stop_loss_pct = 0.052
#sell_sma_period = 40


# get historical OHLCV data for past 200 periods
ohlcv = exchange.fetch_ohlcv(symbol, timeframe = '1m', limit = 200)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# retreive current price of stock
price = exchange.fetch_ticker(symbol)['last']

# calculate the 20 sma using a rolling average of 20
sma_20 = df['close'].rolling(window=20).mean()


# store last (most recent) 20 SMA as a variable
last_sma_20 = sma_20.iloc[-1]

# add the 20 SMA to the main DF
df['sma_20'] = sma_20

# calculate the 40 SMA using a rolling average of 40
sma_40 = df['close'].rolling(window=40).mean()

# store last (most recent) 40 SMA as a variable
last_sma_40 = sma_40.iloc[-1]

# add the 40 SMA to the main DF
df['sma_40'] = sma_40


# Output
print(df)
print(f'this is {symbol} current price {price} and sma_period {sma_20}')

# Initialize a variable to TRACK wheter you are in a postion or not
in_positon = False

# retreive your balance from the exchange
balance = exchange.fetch_balance()

# check if you have a non_zero balance of BTC/stock
if balance['AAPL']['free'] > 0:
    # if you do, set the in postion to TRUE
    in_positon = True

# check the curent price is ABOVE the 20 sma
if df['close'].iloc[-1] > last_sma_20:
    # if so, and your are NOT in postion, buy that ho
    if not in_positon:
        # (Define the amount of BTC/stock to buy at a given price)
        exchange.create_order(symbol, 'market', 'buy', amount, df['close'].iloc[-1])

        # set the in_postion to TRUE
        in_positon = True

    # Hold the Stock for at leaset 5 days
    start_time = time.time()
    while time.time() - start_time < 5 * 24 * 60 * 60:
        # sleep for about a min
        time.sleep(60)



# check if the current price is below the 40 SMA
if df['close'].iloc[-1] < last_sma_40:
    # if so, sell that ho
    # (defining amount of BTC/stock with given price to sell)
    exchange.create_order(symbol, 'market', 'sell', amount, df['close'].iloc[-1])


import schedule
# loop the bot forever
schedule.every(1).seconds.do(bot)

while True:
    try: 
        schedule.run_pending()
    except:
        print('##### PERRO THERE iS AN ERROR #### ')
        print('##### PERRO THERE iS AN ERROR #### ')
        print('##### PERRO THERE iS AN ERROR #### ')
        time.sleep(30)
