import os

# 
capital_range = [{"range_name": "small", "lower": 250000000, "upper": 2000000000},
                 {"range_name": "mid", "lower": 2000000000, "upper": 10000000000},
                 {"range_name": "large", "lower": 10000000000, "upper": 200000000000},
                 {"range_name": "mega", "lower": 200000000000, "upper": 20000000000000000}
                ]
                 

sector_list_ticker = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]

# Set environment variables
os.environ["DATABASE_URL"] = "mongodb://localhost:27017/"
os.environ["FTP_SERVER"] = "ftp.nasdaqtrader.com"
os.environ["SAVE_PATH"] = "./tickers/ticker_table"
os.environ["TARGET_PATH"] = "./tickers/ticker_table/nasdaqlisted.txt"
os.environ["sector_list"] = ','.join(sector_list_ticker)
os.environ["capital_range"] = str(capital_range)
