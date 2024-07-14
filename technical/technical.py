import pandas as pd
from database import find_all
import sys
import matplotlib.pyplot as plt
import os 
sys.path.append("..")
from tickers import all_ticker_list
from database import bulk_insert
from database import db


class Technical:
    def __init__(self):
        self.classified_by_market_size = self.classify_by_market_size()
        
    def classify_by_market_size(self):
        ticker_ranges = eval(os.environ["capital_range"])
        tempObj = {}
        for ticker_range in ticker_ranges:
            query = {"marketCap": {"$gt": ticker_range["lower"], "$lt": ticker_range["upper"]}}
            projection = {"marketCap": 1, "symbol": 1 , "_id": 0}
            result = db["all_ticker_info"].find(query, projection)
            tempObj[ticker_range["range_name"]] = list(result)
        return tempObj
    
    def classify_by_market_sector(self):
        pass
    
    def find_all_sector(self):
        projection = {"sector": 1, "industry": 1}
        documents = db['all_ticker_info'].find({}, projection)
        resultArray = []
        for document in documents:
            try:
                if document["sector"] not in resultArray:
                    resultArray.append(document["sector"])
            except Exception as e:
                print("Exception", e)

    def find_all_industry(sector):
        projection = {"sector": 1, "industry": 1}
        documents = db['all_ticker_info'].find({}, projection)
        resultObj = {}
        for document in documents:
            try:
                if document["sector"] in resultObj:
                    if(document["industry"] not in resultObj[document["sector"]]):
                        resultObj[document["sector"]].append(document["industry"])
                else:
                    resultObj[document["sector"]] = [document["industry"]]
            except Exception as e:
                print("Exception", e)
        print("resultObj", resultObj)

    
    def classify_by_sector(self):
        all_sector = eval(os.environ["sector_list"])
        resultObj = {}
        for item in all_sector:
            query = {"sector": item}
            projection = {"symbol": 1, "_id": 0}
            documents = db['all_ticker_info'].find(query, projection)
            resultObj[item] = list(documents)
        return resultObj
            

    def ticker_movingAverage(self, ticker, period):
        try:
            documents = find_all(ticker + "_daily_history")
            tempArray = []
            pdData = pd.DataFrame(documents)
            SMA_field = "SMA" + str(period)
            pdData[SMA_field] = pdData["close"].rolling(window=period).mean()
            pdData.dropna(inplace=True)
            return pdData
        except Exception as e:
            print("Error in ticker_movingAverage", e)

    def compareTwoAverageLine(self, first_moving_average, second_moving_average):
        merged_df = first_moving_average.merge(second_moving_average, on="date", how="inner")
        print(merged_df.columns.tolist())
        plt.plot(merged_df["date"], merged_df["SMA20"], label="SMA 20", color="blue")
        plt.plot(merged_df["date"], merged_df["SMA50"], label="SMA 50", color="red")
        plt.legend()
        plt.show()
        
    def closed_price_above_ma(self, moving_average, field):
        average = moving_average.tail(1)[field]
        closed = moving_average.tail(1)["close"]
        comparison = closed > average
        any_comparison = comparison.any()
        return any_comparison
        
    
    def sector_performance(self):
        test_data = {
            "Technology": [{"symbol": "AAPL"}]
        }
        
        classified_by_sector = self.classify_by_sector()
        # classified_by_sector = test_data
        length = 0
        total_tickers_each_sector = {}
        ticker_that_above_20MA = {}
        sector_above_average_percent = {}
        for key, value in classified_by_sector.items():
            for item in value:
                length+=1 
                try:
                    twenty_day_average = self.ticker_movingAverage(item["symbol"], 20)
                    closed_price_above_average = self.closed_price_above_ma(twenty_day_average, "SMA20")
                    if key in total_tickers_each_sector:
                        total_tickers_each_sector[key] += 1
                    else:
                        total_tickers_each_sector[key] = 1
                    if key in ticker_that_above_20MA:
                        if(closed_price_above_average == True):
                            ticker_that_above_20MA[key] += 1
                    else:
                        ticker_that_above_20MA[key] = 1
                except Exception as e:
                    print("Exception", e)
        print("total_tickers_each_sector", total_tickers_each_sector)
        print("ticker_that_above_20MA", ticker_that_above_20MA)
        for key, value in total_tickers_each_sector.items():
            sector_above_average_percent[key] = ticker_that_above_20MA[key] / total_tickers_each_sector[key]
        print("sector_above_average_percent", sector_above_average_percent)
    
    def find_the_slope(self):
        pass
        
    
    def sector_performance_slope(self):
        print('Hello World')
        test_tickers = ['AAPL']
        for ticker in test_tickers:
            document = find_all(ticker + "_daily_history")
            df = pd.DataFrame(document)
            df["slope"] = df["close"] - df["close"].shift(1)
        print('df', df.tail())
                       
                