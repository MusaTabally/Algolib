#Import test data
import yfinance as yf
import pandas as pd
import os

class AlgoTrade:
    
    def __init__(self, ticker, data=None):
        self.ticker = ticker
        self.stock_info = yf.Ticker(self.ticker).info
        self.current_price = self.stock_info["currentPrice"]
        self.data = data if data is not None else self.fetchData(self.ticker)[1]
        self.signal = self.signal_generator() 
        self.data["signal"] = self.signal

    def fetchData(self,ticker):
        dataF = yf.download(ticker, period="7d", interval='1d')
        dataF.iloc[:,:]
        self.data = dataF
        return [ticker,dataF]
    
    def saveData(self):
        data = self.getData()
        location = self.ticker+"_data.csv"
        data.to_csv(location)
        return location

    def readData(self,ticker):
        if os.path.exists(ticker+"_data.csv") == False:
            self.data = self.saveData(ticker)

        with open(ticker+"_data.csv") as f:
            dataF = pd.read_csv(f)
        return dataF

    def signal_generator(self):
        df = self.data
        if len(df) < 2:
            return 0 

        # Latest and previous day's data
        latest_open = df['Open'].iloc[-1]
        latest_close = df['Close'].iloc[-1]
        prev_open = df['Open'].iloc[-2]
        prev_close = df['Close'].iloc[-2]

        # Bearish Pattern
        if latest_open > latest_close and prev_close > prev_open:
            self.signal = 1 
        # Bullish Pattern
        elif latest_open < latest_close and prev_close < prev_open:
            self.signal = 2
        # No clear pattern
        else:
            self.signal = 0
        
        self.json = {
            'ticker': self.ticker,
            "current_price": self.current_price,
            "data": self.data.to_json(),
            'signal': self.signal,
            'latest_open': latest_open,
            'latest_close': latest_close,
            'previous_open': prev_open,
            'previous_close': prev_close
        }
        return self.signal

    def getSignal(self):
        return self.signal  
    
    def getData(self):
        return self.data
    
    def getJSON(self):
        return self.json


if __name__ == "__main__":
    ticker = input("Enter ticker: ")
    save = input("Save data? (y/n): ")
    algo = AlgoTrade(ticker)
    print(algo.getJSON())
    if save == "y":
        algo.saveData(ticker)
