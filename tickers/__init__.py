from .ticker import Tickers

tickers_instance = Tickers()
# tickers_instance.get_all_tickersFunc()
# tickers_instance.all_ticker_info()
# tickers_instance.all_ticker_history("5y")
tickers_instance.all_ticker_fundamentals()


