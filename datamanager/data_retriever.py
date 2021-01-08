import pandas as pd
import numpy as np
import sqlite3 as sql
import time
import matplotlib.pyplot as plt
import os


"""
V 1.0
Gets Ticker list
Creates query to access data
"""





class TickerList:
    #Returns stock list as list


    def ticker_list(self, conn):
            
        table_lst = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")

        table_lst = [i[0] for i in table_lst.fetchall()]

        #Must return list of tickers that are located in DB
        return table_lst

    
    def approved_tickers(self):
        raise NotImplemented

    
class GetFrame(TickerList):
    #Generates query to get stock info from DB

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

    def __init__(self):
        super().__init__()

    #Checks if ticker is in DB
    def ticker_is_valid(self, ticker, time_frame, conn):

        ticker = f'{ticker}_{time_frame}'

        if ticker not in self.ticker_list(conn):
            raise Exception(f'{ticker} Ticker is not in the list')

        if time_frame not in self.ACCEPTED_TIME_FRAMES:
            raise Exception(f'Time frame for "{ticker} is not supported"')

        return True

    #Checks if column exists
    def validate_column(self, col, col_lst):

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
            