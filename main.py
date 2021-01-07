"""
1. Creates DB
2. Downloads asset data
3. Maintains DB
"""
import os

from datamanager.database_manager import Connector
from datamanager.database_manager import StockConnector

from datamanager.modules.tickers import RussianStockTickers


if __name__ == "__main__":

    stock_path = StockConnector().get_path

    ticker_list = RussianStockTickers().get_tickers

    with Connector(stock_path) as stock_conn:
        print('Hello world')
        print(ticker_list)

    
    
