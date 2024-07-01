from schedule import schedule_instance
from tickers import tickers_instance
from database import database
import pymongo


tickers_instance.update_all_ticker_price_history()