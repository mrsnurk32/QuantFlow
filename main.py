"""
1. Creates DB
2. Downloads asset data
3. Maintains DB
"""
import os
import asyncio

from datamanager import Connector, StockConnector, \
    DownloadAsset ,UpdateAsset, DB_Checker, AssetConfig

from datamanager import RussianStockTickers

import MetaTrader5 as mt5

import time

from datetime import datetime as dt
from datetime import timedelta


if __name__ == "__main__":

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    stock_path = StockConnector().get_path

    ticker_list = RussianStockTickers().get_tickers

    time_frames = AssetConfig().time_frames
    
    with Connector(stock_path) as stock_conn:

        while True:
            downloadloop = asyncio.get_event_loop()
            tasks = list()

            for ticker in ticker_list:

                for tf in time_frames:

                    if DB_Checker.get_update(conn = stock_conn, ticker = ticker, time_frame = tf):

                        tasks.append(
                            downloadloop.create_task(
                                UpdateAsset().update_mt_asset(
                                    ticker = ticker, tf = tf, conn = stock_conn
                                )   
                            )
                        )
                        

                    else:

                        tasks.append(
                            downloadloop.create_task(
                                DownloadAsset().download_mt_asset(
                                    ticker = ticker, tf = tf, conn = stock_conn
                                )   
                            )
                        )
            
            if len(tasks) > 0:
                wait_tasks = asyncio.wait(tasks)
                downloadloop.run_until_complete(wait_tasks)
                downloadloop.close()

            now = dt.now()
            next_update = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours = 1)
            sleep_time = (next_update - now).total_seconds()

            print(f'seconds {sleep_time} until next update')

            time.sleep(sleep_time)