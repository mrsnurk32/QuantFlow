"""
V 1.1
Establishes DB connection
StockConnector establishes connection with stock db
CurrencyConnectro establishes connection with currency db
"""

import sqlite3 as sql

from .file_checker import FileCheck


class Connector:
    
    """
    1. Establishes connection with db
    2. Close connection with db
    """
    
    def __init__(self, directory):
        self.directory = directory


    def __enter__(self):

        FileCheck().check_files

        self.conn = sql.connect(self.directory)
        return self.conn
        
    def __exit__(self,exc_type,exc_value, exc_tb):

        if self.conn:
            self.conn.close()


class Directrory:

    """
    1. Returns directory of DataBase
    """

    @property
    def get_path(self):
        return self.directory



class StockConnector(Directrory):
    #path to stock_data
    def __init__(self):
        self.directory = 'asset_data/stock_data.db'


class CurrencyConnector(Directrory):
    #path to currency_data
    def __init__(self):
        self.directory = 'asset_data/currency_data.db'

