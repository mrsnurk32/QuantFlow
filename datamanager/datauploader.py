from data_base_manager import Connector, MT_MOEX_Stocks, commit_handler , Tickers_in_db
from data_uploader import mt_from, mt_interval, time_frames, format_data

from modules import approved_tickers
import MetaTrader5 as mt5

import time

import threading
__all__ = ['tasks']



def mt_uploader():

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    t1 = time.perf_counter()
    with Connector(MT_MOEX_Stocks().get_path) as conn:

        for ticker in approved_tickers:
            for time_frame in time_frames:
                ticker_ = f'{ticker}_{time_frame}'
                params = {'conn':conn,'ticker':ticker_}
                
                if ticker_ not in Tickers_in_db(conn):
                    frame = format_data(mt_from(ticker, time_frame))
                    params |= {'frame':frame, 'update':False}

                else:
                    data = mt_interval(ticker, time_frame, conn)
                    if data is None: continue
                    frame = format_data(data)
                    params |= {'frame':frame, 'update':True}

                commit_handler(**params)

# To implement
# 1. Data Check
# 2. Profiling
# 3. Testing
            
    t2 = time.perf_counter()
    print(t2 - t1)
