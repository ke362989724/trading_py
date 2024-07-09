import pandas as pd
from database import find_all
import sys
import matplotlib.pyplot as plt
import os 
sys.path.append("..")
from tickers import all_ticker_list


class Technical:

    def ticker_movingAverage(self, ticker, period):
        try:
            documents = find_all(ticker + "_daily_history")
            tempArray = []
            pdData = pd.DataFrame(documents)
            SMA_field = "SMA" + str(period)
            pdData[SMA_field] = pdData["close"].rolling(window=period).mean()
            pdData.dropna(inplace=True)
            return pdData
            print("pdData", pdData.head())
            plt.plot(pdData["date"], pdData["close"], label="Close Price", color="blue")
            plt.plot(pdData["date"], pdData[SMA_field], label="SMA", color="red")
            plt.title(f"{ticker} Moving Average")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.legend(loc="upper left")
            plt.show()
        except Exception as e:
            print("Error in ticker_movingAverage", e)

    
    def sector_performance(self):
        ticker_range = eval(os.environ["capital_range"])
        print("ticker_range", ticker_range)
        print("all_ticker_list", all_ticker_list)
        for item in all_ticker_list:
            try:
                documents_daily_price = find_all(item + "_daily_history")
                documents_info = find_all(item + "_info")

            except Exception as e:
                print("Error in sector_performance", e)

    def sector_performance_slope(self):
        pass
