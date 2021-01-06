"""
1. Creates DB
2. Downloads asset data
3. Maintains DB
"""
import os

from datamanager.database_manager import Connector
from datamanager.database_manager import StockConnector



if __name__ == "__main__":

    stock_path = StockConnector().get_path

    with Connector(stock_path) as stock_conn:
        print('Hello world')

    
    
