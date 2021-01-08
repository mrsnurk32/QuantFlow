"""
1. Creates DB
2. Downloads asset data
3. Maintains DB
"""
import os
import asyncio

from datamanager import Connector, StockConnector, \
    DownloadAsset ,UpdateAsset, DB_Checker


from datamanager import RussianStockTickers



import MetaTrader5 as mt5



if __name__ == "__main__":

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    stock_path = StockConnector().get_path

    ticker_list = RussianStockTickers().get_tickers
    
    with Connector(stock_path) as stock_conn:

        downloadloop = asyncio.get_event_loop()
        tasks = list()

        for ticker in ticker_list:

            if DB_Checker.get_update(conn = stock_conn, ticker = ticker):

                tasks.append(
                    downloadloop.create_task(
                        UpdateAsset().update_mt_asset(
                            ticker = ticker, tf = '1h', conn = stock_conn
                        )   
                    )
                )
                

            else:

                tasks.append(
                    downloadloop.create_task(
                        DownloadAsset().download_mt_asset(
                            ticker = ticker, tf = '1h', conn = stock_conn
                        )   
                    )
                )
        
        if len(tasks) > 0:
            wait_tasks = asyncio.wait(tasks)
            downloadloop.run_until_complete(wait_tasks)
            downloadloop.close()

            




    
    
