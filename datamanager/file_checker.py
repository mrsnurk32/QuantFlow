"""
V 2.0
This module check the file system and creates files if missing
"""

import os
from datetime import datetime as dt
from .modules import time_frames
# from .data_retriever import GetFrame
# from .download_asset import VerifyData
import pandas as pd
import asyncio

# class DataChecker(VerifyData, GetFrame):


#     def get_db_data(self, conn, ticker, time_frame):

#         return self.get_frame(
#             conn = conn, ticker = ticker,
#             time_frame = time_frame, rows = 500
#         )


#     def get_verified_data(self, ticker, time_frame):
#         return self.verify_data(
#             ticker = ticker, time_frame = time_frame, 
#             rows = 500
#         )


#     def compare_data(self, local_copy, global_copy):

#         #temp solution

#         o = list(local_copy.open.values) == list(global_copy.open.values)
#         c = list(local_copy.close.values) == list(global_copy.close.values)
        
#         return o and c


#     def init_check(self, conn, ticker, time_frame):

#         if dt.now().hour > 8:
#             return False

#         else:
#             print(f'Checking {ticker} ({time_frame})')
#             local_copy = self.get_db_data(conn = conn, ticker = ticker, time_frame = time_frame)
#             global_copy = self.get_verified_data(ticker = ticker, time_frame = time_frame)
#             return self.compare_data(local_copy, global_copy)




def check_for_update(conn, tickers):

    """
        The function returns true if asset exists in db to initialize update
    if data is not present in db it will return false to initialize download method 
    """
        
    table_lst = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    table_lst = [i[0] for i in table_lst.fetchall()]

    download = list()
    update = list()

    for ticker in tickers:
        for time_frame in time_frames:
            full_ticker = f"{ticker}_{time_frame}"
            if full_ticker in table_lst:
                update.append(full_ticker)
            else:
                download.append(full_ticker)

    return {
        'update':update,
        'download':download,
    }
        


class FileCheck:

    """
    1. Checks for database directory
    2. Creates one if missing
    """
    
    DIRECTORIES = (
        'asset_data',
    )

    @property
    def check_files(self):

        file_list = os.listdir()
        for _dir in self.DIRECTORIES:
            if _dir not in file_list:
                print(f'created {_dir}')
                os.mkdir(_dir)
            



