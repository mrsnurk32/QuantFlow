"""
V 2.0
This module check the file system and creates files if missing
"""

import os
from datetime import datetime as dt
from .data_retriever import GetFrame
import pandas as pd
import asyncio


class TableManager:

    def delete_last_n_rows(self, conn, asset):
        ticker, time_frame = asset.split('_')[0], asset.split('_')[1]
        table = f'{ticker}_{time_frame}'

        query = f"""delete from {table} where rowid IN 
            (SELECT rowid from {table} order by rowid desc limit {500})"""
        
        conn.execute(query)
        conn.commit()

    
    def fix_update(self, asset, conn):
        ticker, time_frame = asset.split('_')[0], asset.split('_')[1]
        self.update_mt_asset(ticker = ticker, time_frame = time_frame,
        conn = conn)


class DataChecker(VerifyData, GetFrame, TableManager):


    def get_db_data(self, conn, ticker, time_frame):

        return self.get_frame(
            conn = conn, ticker = ticker,
            time_frame = time_frame, rows = 500
        )


    def get_verified_data(self, ticker, time_frame, last_date):
        return self.verify_data(
            ticker = ticker, time_frame = time_frame, 
            rows = 500, last_date = last_date
        )


    def compare_data(self, local_copy, global_copy):

        #temp solution

        o = list(local_copy.open.values) == list(global_copy.open.values)
        c = list(local_copy.close.values) == list(global_copy.close.values)
        
        return o and c


    def init_check(self, conn, ticker, time_frame):

        print(f'Checking {ticker} ({time_frame})')
        local_copy = self.get_db_data(conn = conn, ticker = ticker, time_frame = time_frame)
        last_date = local_copy.time.iloc[-1]
        global_copy = self.get_verified_data(ticker = ticker, time_frame = time_frame, last_date = last_date)
        return self.compare_data(local_copy, global_copy)



def check_data(ticker_list, time_frames, conn):

    checker = DataChecker()
    print('Checking Data!')
    err_list = list()

    for ticker in ticker_list:

        for tf in time_frames:

            result = checker.init_check(
                conn = conn, ticker = ticker, time_frame = tf
                )
            
            if result is False:
                err_list.append(ticker + '_' + tf)


            print(ticker,tf, result)
    print('error list')
    print(err_list)

    for asset in err_list:
        checker.delete_last_n_rows(
            conn = conn, asset = asset)

        checker.fix_update(
            conn = conn, asset = asset
        )



class DB_Checker:
    #checks for asset data in db

    @staticmethod
    def get_update(conn, ticker, time_frame):

        """
            The function returns true if asset exists in db to initialize update
        if data is not present in db it will return false to initialize download method 
        """
            
        table_lst = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        table_lst = [i[0] for i in table_lst.fetchall()]
        ticker = f'{ticker}_{time_frame}'

        if ticker in table_lst:
            return True

        else:
            return False
        


# class FileCheck:

#     """
#     1. Checks for database directory
#     2. Creates one if missing
#     """
    
#     DIRECTORIES = (
#         'asset_data',
#     )

#     @property
#     def check_files(self):

#         file_list = os.listdir()
#         for _dir in self.DIRECTORIES:
#             if _dir not in file_list:
#                 print(f'created {_dir}')
#                 os.mkdir(_dir)
            


