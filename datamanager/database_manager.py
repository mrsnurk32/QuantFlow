"""
V 1.0
Establishes DB connection
"""

import sqlite3 as sql


class Connector:
    
    #The class establishes connection with DB.

    @staticmethod
    def connect_to_db(directory):

        sqlite3_conn = None

        try:

            sqlite3_conn = sql.connect(directory)
            return sqlite3_conn
        
        except Exception as err:

            print(err)
            if sqlite3_conn is not None:
                sqlite3_conn.close()


class StockConnector:
    # The class establishes connection with stock db
    directory = 'asset_data/stock_data.db'

    @property
    def establish_connection(self):
        return Connector().connect_to_db(self.directory)


class CurrencyConnector:
    # The class establishes connection with stock db
    directory = 'asset_data/currency_data.db'

    @property
    def establish_connection(self):
        return Connector().connect_to_db(self.directory)
