import ftplib
import os.path
import yfinance as yf
import sys
sys.path.append("..")
from database import bulk_insert
from database import db
from database import insert_one
from schedule import schedule_instance
import pymongo
import pytz


class Tickers:
    def __init__(self):
        self.save_path = os.environ["SAVE_PATH"]
        self.targetPath = os.environ["TARGET_PATH"]
        self.max_huck_size = 16 * 1024 * 1024
        self.all_ticker_list = self.all_ticker_list()
        self.split_ticker_into_chunks(100)
    def get_all_tickersFunc(self) -> int:
        ftp_server = ftplib.FTP(os.environ["FTP_SERVER"])
        ftp_server.login()
        ftp_server.encoding = "utf-8"

        save_path = self.save_path

        filenames = ["nasdaqlisted.txt"]

        ftp_server.cwd('Symboldirectory')
        ftp_server.dir()
        
        for filename in filenames:
            complete_path = os.path.join(save_path, filename)
            with open(complete_path, "wb") as file:
                ftp_server.retrbinary(f"RETR {filename}", file.write)

        ftp_server.quit()
        self.remove_lines(self.targetPath, 1)
        
        
    def remove_lines(self, targetPath, linesToRemove):
        with open(targetPath, "r") as file:
            lines = file.readlines()

        modified_lines = lines[linesToRemove:]

        with open(targetPath, "w") as file:
            file.writelines(modified_lines)
            
    def all_ticker_list(self):
        targetPath = self.targetPath
        ticker_list = []
        with open(targetPath, "r") as file:
            for line in file:
                try:
                   ticker_list.append(line.split("|")[0]) 
                except Exception as e:
                    print("An exception occurred", e)
        return ticker_list
        
            
    def split_ticker_into_chunks(self, chunk_size):
        result_array = []
        for i in range(0, len(self.all_ticker_list), chunk_size):
            result_array.append(self.all_ticker_list[i:i+chunk_size])
        self.splitted_ticker_chunk_list =  result_array

    def all_ticker_info(self):
        targetPath = self.targetPath
        data = []       
        with open(targetPath, "r") as file:
            for item in self.all_ticker_list:
                try:
                    responseData = yf.Ticker(item).info
                    bulk_insert([responseData], item + "_info")
                except Exception as e:
                    print("An exception occurred", e)
        
    def all_ticker_history(self, period):
        test_data = self.s
        for item in test_data:
            tempArray = []
            try:
                responseData = yf.Ticker(item).history(period=period)
                for key, value in responseData.iterrows():
                    tempObj = {}
                    tempObj["open"] = value["Open"].item()
                    tempObj["high"] = value["High"].item()
                    tempObj["low"] = value["Low"].item()
                    tempObj["close"] = value["Close"].item()
                    tempObj["dividends"] = value["Dividends"].item()
                    tempObj['date'] = key.to_pydatetime()
                    tempArray.append(tempObj)
            except Exception as e:
                print("error", e)
            print("tempArray", tempArray)
            bulk_insert(tempArray, item + "_daily_history")
            
            
    def all_ticker_fundamentals(self):
        test_data = self.all_ticker_list
        for item in test_data:
            responseData = yf.Ticker(item)
            responseData_income_stmt = responseData.income_stmt
            self.loop_out_ticker(responseData_income_stmt, item + "_income_statement")
            responseData_quarterly_income_stmt = responseData.quarterly_income_stmt
            self.loop_out_ticker(responseData_quarterly_income_stmt, item + "_quarterly_income_stmt")
            responseData_balance_sheet = responseData.balance_sheet
            self.loop_out_ticker(responseData_balance_sheet, item + "_balance_sheet")
            responseData_quarterly_balance_sheet = responseData.quarterly_balance_sheet
            self.loop_out_ticker(responseData_quarterly_balance_sheet, item + "_quarterly_balance_sheet")
            responseData_cash_flow = responseData.cashflow
            self.loop_out_ticker(responseData_cash_flow, item + "_cash_flow")
    
    def loop_out_ticker(self, responseData, target_table_name):
        tempArray = []
        for column in responseData.columns:
            tempObj = {
                "date": column.to_pydatetime(),
            }
            for index, value in responseData[column].items():
                tempObj[index] = value
            tempArray.append(tempObj)
        bulk_insert(tempArray, target_table_name)
        
    def update_all_ticker_price_history(self):
        test_data = self.splitted_ticker_chunk_list
        print("test_data", test_data)
        for item1 in test_data:
            print(item1, "item1")
            tickers = yf.Tickers(", ".join(item1))
            print("tickers", tickers)
            for item2 in item1:
                try:
                    temp_data = tickers.tickers[item2].history(period="5d")
                    print("temp_data", temp_data)
                    for key, value in temp_data.iterrows():
                        tempObj = {}
                        tempObj["open"] = value["Open"].item()
                        tempObj["high"] = value["High"].item()
                        tempObj["low"] = value["Low"].item()
                        tempObj["close"] = value["Close"].item()
                        tempObj["dividends"] = value["Dividends"].item()
                        tempObj['date'] = key.to_pydatetime()
                        dbData = db[item2 + "_daily_history"].find_one({}, sort=[("date", pymongo.DESCENDING)])
                        db_date = pytz.utc.localize(dbData["date"]).date()
                        tempObj_date = tempObj["date"].replace(tzinfo=pytz.utc).date()
                        if(tempObj_date > db_date):
                            insert_one(tempObj, item2 + "_daily_history")
                            print(item2, "new data is inserted")
                        else:
                            print(item2, "latest data is inserted")
                except Exception as e:
                    print("error", e)


    def ticker_price_history(self, ticker, period):
        spy_ticker = yf.Ticker(ticker)
        responseData = spy_ticker.history(period=period)
        tempArray = []
        try:
            for key, value in responseData.iterrows():
                tempObj = {}
                tempObj["open"] = value["Open"].item()
                tempObj["high"] = value["High"].item()
                tempObj["low"] = value["Low"].item()
                tempObj["close"] = value["Close"].item()
                tempObj["dividends"] = value["Dividends"].item()
                tempObj['date'] = key.to_pydatetime()
                tempArray.append(tempObj)
        except Exception as e:
            print("error", e)
            print("tempArray", tempArray)
        
        bulk_insert(tempArray, ticker + "_daily_history")

    

    def sector_list_price_history(self):
        sector_list = os.environ["sector_list"].split(",")
        for item in sector_list:
            responseData = yf.Ticker(item).history(period="5y")
            tempArray = []
            for key, value in responseData.iterrows():
                tempObj = {}
                tempObj["open"] = value["Open"].item()
                tempObj["high"] = value["High"].item()
                tempObj["low"] = value["Low"].item()
                tempObj["close"] = value["Close"].item()
                tempObj["dividends"] = value["Dividends"].item()
                tempObj['date'] = key.to_pydatetime()
                tempArray.append(tempObj)
            bulk_insert(tempArray, item + "_daily_history")