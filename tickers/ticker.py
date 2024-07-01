import ftplib
import os.path
import yfinance as yf
import sys
sys.path.append("..")
from database import bulk_insert


class Tickers:
    def __init__(self, item):
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
        test_data = ["AAPL"]

        