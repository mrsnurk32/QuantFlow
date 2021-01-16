from data_base_manager import Connector, MT_MOEX_Stocks, commit_handler , Tickers_in_db
from data_uploader import mt_from, mt_interval, time_frames, format_data

from modules import approved_tickers
import MetaTrader5 as mt5

import time

import cProfile
__all__ = ['mt_uploader']



def mt_update_db():

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    with Connector(MT_MOEX_Stocks().get_path) as conn:
        
        conn = conn.cursor()


        for ticker in Tickers_in_db(conn):

            params = {'conn':conn,'ticker':ticker}
            time_frame = ticker.split('_')[-1]
            
            data = mt_interval(ticker, time_frame, conn)
            if data:

                frame = format_data(data)
                params |= {'frame':frame, 'update':True}

                commit_handler(**params)

# To implement
# 1. Data Check
# 2. Profiling
# 3. Testing
# 4. get rid off pandas in this package


if __name__ == '__main__':
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()

    mt_update_db()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
# print('test')
