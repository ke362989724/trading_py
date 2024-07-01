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
        self.save_path = "C:/Users/ke362/Desktop/swing_trade/tickers/ticker_table"
        self.targetPath = "C:/Users/ke362/Desktop/swing_trade/tickers/ticker_table/nasdaqlisted.txt"
        self.max_huck_size = 16 * 1024 * 1024
        self.all_ticker_list = self.all_ticker_list()
    def get_all_tickersFunc(self):
        ftp_server = ftplib.FTP("ftp.nasdaqtrader.com")
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
        targetPath = "C:/Users/ke362/Desktop/swing_trade/tickers/ticker_table/nasdaqlisted.txt"
        self.remove_lines(targetPath, 1)
        
        
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
        
            
    def all_ticker_info(self):
        targetPath = self.targetPath
        data = []       
        with open(targetPath, "r") as file:
            for item in self.all_ticker_list:
                try:
                    responseData = yf.Ticker(item).info
                    print("responseData", responseData)
                    data.append(responseData)
                except Exception as e:
                    print("An exception occurred", e)
        bulk_insert(data, "tickers")
        
    def all_ticker_history(self, period):
        test_data = self.all_ticker_list
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
        test_data = self.all_ticker_list
        for item in test_data:
            try:
                responseData = yf.Ticker(item).history(period="1d")
                for key, value in responseData.iterrows():
                    tempObj = {}
                    tempObj["open"] = value["Open"].item()
                    tempObj["high"] = value["High"].item()
                    tempObj["low"] = value["Low"].item()
                    tempObj["close"] = value["Close"].item()
                    tempObj["dividends"] = value["Dividends"].item()
                    tempObj['date'] = key.to_pydatetime()
                    dbData = db[item + "_daily_history"].find_one({}, sort=[("date", pymongo.DESCENDING)])
                    db_date = pytz.utc.localize(dbData["date"]).date()
                    tempObj_date = tempObj["date"].replace(tzinfo=pytz.utc).date()
                    if(tempObj_date > db_date):
                        insert_one(tempObj, item + "_daily_history")
                        print("Date bigger , data is most updated")
                    else:
                        print("Date smaller , data is most updated")
            except Exception as e:
                print("error", e)
            