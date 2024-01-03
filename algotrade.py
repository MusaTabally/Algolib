#Import test data
import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2022-10-7", end="2022-12-5", interval='15m')
dataF.iloc[:,:]
#dataF.Open.iloc

#define signal function
def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish Pattern
    if (open>close and 
    previous_open<previous_close and 
    close<previous_open and
    open>=previous_close):
        return 1

    # Bullish Pattern
    elif (open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close):
        return 2
    
    # No clear pattern
    else:
        return 0

signal = []
signal.append(0)
for i in range(1,len(dataF)):
    df = dataF[i-1:i+1]
    signal.append(signal_generator(df))
#signal_generator(data)
dataF["signal"] = signal

dataF.signal.value_counts()
#dataF.iloc[:, :]
#connect to market
'''from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from config import access_token, accountID'''
def get_candles(n):
    #access_token='XXXXXXX'#you need token here generated from OANDA account
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o))>1)

def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])
    
    i=0
    for candle in candles:
        dfstream.loc[i, ['Open']] = float(str(candle.bid.o))
        dfstream.loc[i, ['Close']] = float(str(candle.bid.c))
        dfstream.loc[i, ['High']] = float(str(candle.bid.h))
        dfstream.loc[i, ['Low']] = float(str(candle.bid.l))
        i=i+1

    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    signal = signal_generator(dfstream.iloc[:-1,:])#
    
    # EXECUTING ORDERS
    #accountID = "XXXXXXX" #your account ID here
    client = API(access_token)
         
    SLTPRatio = 2.
    previous_candleR = abs(dfstream['High'].iloc[-2]-dfstream['Low'].iloc[-2])
    
    SLBuy = float(str(candle.bid.o))-previous_candleR
    SLSell = float(str(candle.bid.o))+previous_candleR

    TPBuy = float(str(candle.bid.o))+previous_candleR*SLTPRatio
    TPSell = float(str(candle.bid.o))-previous_candleR*SLTPRatio
    
    print(dfstream.iloc[:-1,:])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)
    signal = 2
    #Sell
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000, takeProfitOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    #Buy
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data, stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
#Exucuting oreders automatically 
trading_job()

#scheduler = BlockingScheduler()
#scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
#scheduler.start()
'''
import yfinance as yf
import pandas as pd

# Fetch data from Yahoo Finance
def fetch_data(symbol, start_date, end_date, interval):
    df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return df

# Calculate moving averages
def calculate_moving_averages(df, short_window, long_window):
    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()
    return df

# Generate trading signals
def generate_signals(df):
    signals = []
    for i in range(len(df)):
        if df['SMA_Short'].iloc[i] > df['SMA_Long'].iloc[i] and \
           df['SMA_Short'].iloc[i-1] <= df['SMA_Long'].iloc[i-1]:
            signals.append('Buy')
        elif df['SMA_Short'].iloc[i] < df['SMA_Long'].iloc[i] and \
             df['SMA_Short'].iloc[i-1] >= df['SMA_Long'].iloc[i-1]:
            signals.append('Sell')
        else:
            signals.append('Hold')
    df['Signal'] = signals
    return df

# Main function to run the strategy
def run_strategy(symbol, start_date, end_date, interval, short_window, long_window):
    df = fetch_data(symbol, start_date, end_date, interval)
    df = calculate_moving_averages(df, short_window, long_window)
    df = generate_signals(df)
    return df

# Example usage
symbol = "EURUSD=X"
start_date = "2022-01-01"
end_date = "2022-12-31"
interval = '1d'  # Daily interval
short_window = 50  # Short-term moving average window
long_window = 200  # Long-term moving average window

df = run_strategy(symbol, start_date, end_date, interval, short_window, long_window)
print(df[['Close', 'SMA_Short', 'SMA_Long', 'Signal']])
  
'''