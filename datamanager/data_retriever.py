
"""
V 1.0
The module Retrieves asset data from database
"""

import pandas as pd
import numpy as np
import sqlite3 as sql
import time
import matplotlib.pyplot as plt
import os
from modules import Tickers


    
class GetFrame:
    #Generates query to get stock info from DB
    """
        Creates queries to extract data from database 
    """

    ACCEPTED_TIME_FRAMES = ('1h', 'd1', 'min5', 'min1')

    COLUMN_LIST = (
        'time','open', 'high', 'low',
        'close', 'tick_volume', 'spread',
        'real_volume'
    )

    #lisf of columns to be deleted if column list == default
    DEFAULT_COLUMN_LIST = (
        'tick_volume', 'spread', 'real_volume'
    )

    MANDATORY_COLUMNS = (
        'time', 'close'
    )


    def ticker_is_valid(self, ticker, time_frame, conn):
        #Checks if ticker is in DB

        ticker = f'{ticker}_{time_frame}'

        if ticker not in Tickers(conn):
            # raise Exception(f'{ticker} Ticker is not in the list')
            return False

        if time_frame not in self.ACCEPTED_TIME_FRAMES:
            raise Exception(f'Time frame for "{ticker} is not supported"')

        return True


    def validate_column(self, col, col_lst):
        #Checks if column exists

        if col not in col_lst:
            raise Exception(f"Column {col} not found in data set \n {self.COLUMN_LIST} - list of acceptable columns")

    
    #gets data and creates pandas frame. column_list takes list or '*' as parameter
    def get_frame(self, conn, ticker, rows=None, time_frame='1h', column_list = '*'):

        if self.ticker_is_valid(ticker, time_frame, conn):

            if type(column_list) is list:

                #Checks if every column is valid for querry
                [self.validate_column(col = col,col_lst = self.COLUMN_LIST) for col in column_list]
                
                #Checks if required columns are present in the list
                [self.validate_column(col = col, col_lst = column_list) for col in self.MANDATORY_COLUMNS]
                column_list = ', '.join(column_list)
            
            else:
                column_list = '*'

            ticker = ticker + '_' + time_frame
            querry = f'SELECT {column_list} FROM {ticker} ORDER BY rowid DESC'

            if rows is not None:
                querry += f' LIMIT {rows}'

            frame = pd.read_sql_query(querry, conn).sort_index(ascending = False)
            frame.reset_index(drop = True, inplace = True)
            frame.time = pd.to_datetime(frame.time)

            return frame

        else:
            return
