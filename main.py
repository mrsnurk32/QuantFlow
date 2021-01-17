"""
1. Creates DB
2. Downloads asset data
3. Maintains DB
"""
import os
import asyncio
import MetaTrader5 as mt5
import pandas as pd

#connection handlers
from datamanager import connector, stock_path

#db
from datamanager import check_for_update

#ticker data
from datamanager import RussianStockTickers, time_frames

#metatrader related modules
from datamanager import mt_from, mt_interval, commit_data

import time

from datetime import datetime as dt
from datetime import timedelta


def update():

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    
    with connector as stock_conn:
        print('ok')

        #get list of approved tickers
        tickers = RussianStockTickers().custom_ticker_list

        tasks = check_for_update(conn = stock_conn, tickers = tickers)
        
        commit_list = list()
        
        for ticker in tasks['download']:
            ticker, time_frame = ticker.split('_')[0],ticker.split('_')[1]
            commit_list.append((mt_from(ticker, time_frame),'download',ticker,time_frame))


        for ticker in tasks['update']:
            ticker, time_frame = ticker.split('_')[0],ticker.split('_')[1]
            
            # commit_list.append((mt_from(ticker, time_frame)))
            result = mt_interval(ticker, time_frame, stock_conn)
            if len(result) > 1:
                print('upd')
                commit_list.append((result ,'update',ticker, time_frame))

        commit_data(stock_conn,commit_list)

        #check data
            
if __name__ == "__main__":
    
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()

    update()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumtime')
    # stats.print_stats()

            #commit
            #check


    #     while True:
    #         downloadloop = asyncio.get_event_loop()
    #         tasks = list()

    #         for ticker in ticker_list:

    #             for tf in time_frames:

    #                 if DB_Checker.get_update(conn = stock_conn, ticker = ticker, time_frame = tf):

    #                     tasks.append(
    #                         downloadloop.create_task(
    #                             UpdateAsset().update_mt_asset(
    #                                 ticker = ticker, time_frame = tf, conn = stock_conn
    #                             )   
    #                         )
    #                     )
                        

    #                 else:

    #                     tasks.append(
    #                         downloadloop.create_task(
    #                             DownloadAsset().download_mt_asset(
    #                                 ticker = ticker, time_frame = tf, conn = stock_conn
    #                             )   
    #                         )
    #                     )
            
    #         if len(tasks) > 0:
    #             wait_tasks = asyncio.wait(tasks)
    #             downloadloop.run_until_complete(wait_tasks)
    #             downloadloop.close()

    #         now = dt.now()
    #         next_update = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours = 1)
    #         sleep_time = (next_update - now).total_seconds()

    #         if dt.now().hour > 8:
    #             time.sleep(sleep_time)
    #             continue

    #         checker = DataChecker()
    #         print('Checking Data!')
    #         err_list = list()

    #         for ticker in ticker_list:

    #             for tf in time_frames:

    #                 result = checker.init_check(
    #                     conn = stock_conn, ticker = ticker, time_frame = tf
    #                     )
                    
    #                 if result is False:
    #                     err_list.append(ticker + '_' + tf)


    #                 print(ticker,tf, result)
    #         print('error list')
    #         print(err_list)
    #         print(f'seconds {sleep_time} until next update')

    #         time.sleep(sleep_time)