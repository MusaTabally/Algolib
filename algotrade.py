#Import test data
import yfinance as yf
import pandas as pd
import os

class AlgoTrade:
    
    def __init__(self, ticker, data=None):
        self.ticker = ticker
        self.data = data if data is not None else self.readData(ticker)
        self.signal = self.signal_generator()  # Call the method without passing DataFrame
        self.data["signal"] = self.signal

    def fetchData(self,ticker):
        dataF = yf.download(ticker, period="1mo", interval='1d')
        dataF.iloc[:,:]
        return [ticker,dataF]
    
    def saveData(self,ticker):
        data = self.fetchData(ticker)
        data[1].to_csv(data[0]+"_data.csv")
        return data[1]

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


        print("Latest open: ", latest_open)
        print("Latest close: ", latest_close)
        print("Previous open: ", prev_open)
        print("Previous close: ", prev_close)
        

        # Bearish Pattern
        if latest_open > latest_close and prev_close > prev_open:
            return 1 
        # Bullish Pattern
        elif latest_open < latest_close and prev_close < prev_open:
            return 2 
        # No clear pattern
        else:
            return 0
        
    def getSignal(self):
        return self.signal  
    
    def getData(self):
        return self.data


if __name__ == "__main__":
    ticker = input("Enter ticker: ")
    algo = AlgoTrade(ticker)
    print(algo.getSignal())
    
