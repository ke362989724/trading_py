import pandas as pd
from database import find_all
import sys
import matplotlib.pyplot as plt
import os 
sys.path.append("..")
from tickers import all_ticker_list
from database import bulk_insert
from database import db
from datetime import datetime


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
    
    def classify_by_industry(self):
        all_industry = eval(os.environ["industry_list"])
        resultObj = {}
        for key, value in all_industry.items():
            resultObj[key] = []
            for item in value:
                tempObj = {}
                query = {"industry": item}
                projection = {"symbol": 1, "_id": 0}
                documents = db["all_ticker_info"].find(query, projection)
                list_document = list(documents)
                tempObj[item] = list_document
                resultObj[key].append(tempObj)
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

    def number_moving_sma_average(self, data, new_field_name, target_field, period):
        try:
            data[new_field_name] = data[target_field].rolling(window=period).mean()
            data.dropna(inplace=True)
            return data
        except Exception as e:
            print("Error in number_moving_sma_average", e)


    def number_moving_ewm_average(self, data, new_field_name, target_field, period):
        try:
            data[new_field_name] = data[target_field].ewm(span=period, adjust=False).mean()
            data.dropna(inplace=True)
            return data
        except Exception as e:
            print("Error in number_moving_sma_average", e)

    def compareTwoAverageLine(self, first_moving_average, second_moving_average):
        merged_df = first_moving_average.merge(second_moving_average, on="date", how="inner")
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

    def new_high_each_sector_chart(self):
        sector_list = eval(os.environ["sector_list"])
        sector_list_data = []
        for sector in sector_list:
            try:
                query = {"sector": sector}
                projection = {}
                documents = db['sector_new_high'].find(query, projection).sort("date", 1)
                ticker_list = list(documents)
                df = pd.DataFrame(ticker_list)
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)
                self.number_moving_sma_average(df, "SMA20", "percent", 20)
                self.number_moving_sma_average(df, "SMA50", "percent", 50)
                self.number_moving_ewm_average(df, "EMA20", "percent", 20)
                self.number_moving_ewm_average(df, "EMA50", "percent", 50)
                # plt.plot(df.index, df["SMA50"], label="SMA50")
                # plt.plot(df.index, df["SMA20"], label="SMA20")
                plt.plot(df.index, df["EMA50"], label="EMA50")
                plt.plot(df.index, df["EMA20"], label="EMA20")
                plt.title(sector)
                plt.xlabel("Date")
                plt.ylabel("Moving Average")
                plt.legend()
                plt.show()
                sector_list_data.append({"name":sector, "data":df})
            except Exception as e:
                print("Exception", e)
        self.strongest_performance_sector(sector_list_data, 5)

    def strongest_performance_sector(self, df_list, sector_number):
        strongest_sector = []
        weakest_performance = 0
        for value in df_list:
            tail_data = value["data"].iloc[-1]
            strongest_sector.append({"sector": value["name"], "percent": tail_data["percent"]})
            weakest_performance = tail_data["percent"]
            # if len(strongest_sector) == sector_number:
            #     break
        print("strongest_sector", strongest_sector)
        
    
    
    def new_high_each_sector(self, date):
        test_data = {
            "Technology": [{"symbol": "AAPL"}]
        }


        # Convert the date object to the desired format
        # classified_by_sector = test_data
        classified_by_sector = self.classify_by_sector()
        total_tickers_each_sector = {}
        ticker_that_new_high = {}
        sector_above_average_percent = {}
        for key, value in classified_by_sector.items():
            for item in value:
                print("item", item)
                try:
                    projection = {"date": 1, "_id": 0, "close": 1, "high": 1}
                    query = {"date": {"$lte": date}}
                    week_day = 5
                    week_number =50
                    limit= week_day * week_number
                    df = pd.DataFrame(list(db[item["symbol"] + "_daily_history"].find(query, projection).sort("date", -1).limit(limit)))
                    print('df', df)
                    largest_close = df["close"].max()
                    last_close_value = df["close"].iloc[-1]
                    if key in total_tickers_each_sector:
                        total_tickers_each_sector[key] += 1
                    else:
                        total_tickers_each_sector[key] = 1
                    if key in ticker_that_new_high:
                        if(largest_close == last_close_value):
                            ticker_that_new_high[key] += 1
                    else:
                        ticker_that_new_high[key] = 1
                except Exception as e:
                    print("Exception", e)
        last_date = df["date"].iloc[0]
        save_db_data = []
        for key, value in total_tickers_each_sector.items():
            sector_above_average_percent[key] = ticker_that_new_high[key] / total_tickers_each_sector[key]
            save_db_data.append({"sector": key, "new_high_number": ticker_that_new_high[key], "percent": sector_above_average_percent[key] * 100, "date": last_date})
        bulk_insert(save_db_data, "sector_new_high")

    def new_high_each_industry(self):
        test_data = {
            "Technology": [{'Consumer Electronics': [{'symbol': "AAPL"}]}]
        }
        industry_list = self.classify_by_industry()
        # industry_list = test_data
        resultObj = {}
        for key1, value1 in industry_list.items():
            resultObj[key1] = {}
            for item1 in value1:
                for key2, value2 in item1.items():
                    resultObj[key1][key2] = 0
                    for item2 in value2:
                        try:
                            projection = {"date": 1, "_id": 0, "close": 1, "high": 1}
                            query = {"marketCap": {"$gt": 2000000000}}
                            week_day = 5
                            week_number =50
                            limit= week_day * week_number
                            df = pd.DataFrame(list(db[item2["symbol"] + "_daily_history"].find(query, projection).sort("date", -1).limit(limit)))
                            largest_close = df["high"].max()
                            last_close_value = df["close"].iloc[-1]
                            if key2 in resultObj[key1]:
                                if(largest_close == last_close_value):
                                    resultObj[key1][key2] += 1
                            else:
                                resultObj[key1][key2] = 1
                        except Exception as e:
                            print("exception", e)
        print("resultObj", resultObj)
    
    
    def find_the_slope(self):
        pass
        
    
    def sector_performance_slope(self):
        test_tickers = ['AAPL']
        for ticker in test_tickers:
            document = find_all(ticker + "_daily_history")
            df = pd.DataFrame(document)
            df["slope"] = df["close"] - df["close"].shift(1)
            print("dataframe", df)
                       

    