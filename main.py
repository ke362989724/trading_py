import config
from schedule import schedule_instance
from tickers import tickers_instance
from database import database
import pymongo
from technical import technical_instance
from datetime import datetime, timedelta


# tickers_instance.get_all_tickersFunc()
# tickers_instance.all_ticker_history("5y")
tickers_instance.all_ticker_fundamentals()
# tickers_instance.update_all_ticker_price_history()
# tickers_instance.spy_price_history()
# loop and print out the split_list
# tickers_instance.sector_list_price_history()
# tickers_instance.ticker_price_history("SPY", "5y")
# tickers_instance.all_ticker_info()
# technical_instance.ticker_movingAverage("SPY", 50)
# technical_instance.ticker_movingAverage("SPY", 200)

# technical_instance.sector_performance()
# technical_instance.find_all_sector("industry")
# technical_instance.find_all_industry()
# technical_instance.sector_performance_slope()
# current_date = datetime.now()
# for i in range(50):
#     current_date = current_date - timedelta(days=1)
# technical_instance.new_high_each_sector(datetime.now())
# technical_instance.new_high_each_industry()
# technical_instance.new_high_each_sector_chart()


