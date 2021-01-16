import MetaTrader5 as mt5

import pytz
from datetime import datetime as dt
from datetime import timedelta

from ..asset_config import asset_config
from ..weekdays import WeekDays

import time 


__all__ = ['mt_from', 'mt_interval']
    
def mt_from(ticker:str, time_frame:str, rows = 50000):

    def get_data(ticker, mt_time_frame, utc_from, rows = 5000):
        return mt5.copy_rates_from(ticker, mt_time_frame, utc_from, rows)

    global asset_config
    configs = asset_config(time_frame, update = False)
        
    ymd = dt.today()
    
    if WeekDays.trading_day():

        delta = timedelta(days = 1)
        ymd = (ymd - delta)

    utc_from = dt(ymd.year, ymd.month, ymd.day, tzinfo=configs['timezone'])
    del configs['timezone']
    del configs['time_frame']
    configs |= dict(utc_from = utc_from, ticker = ticker)

    return get_data(**configs)


def mt_interval(ticker,time_frame,conn):

    def get_data(ticker, mt_time_frame, utc_from, utc_to):
        return mt5.copy_rates_range(ticker, mt_time_frame, utc_from, utc_to)

    global asset_config
    configs = asset_config(time_frame, update = True)

    #getting last ticker`s price date
    # ticker_ = f'{ticker}_{time_frame}'
    query = conn.execute(
                f'SELECT time FROM {ticker} ORDER BY time DESC LIMIT 1;'
            ).fetchall()[0][0]
    #End

    #creating start point for interval
    utc_from = (
            dt.strptime(query,'%Y-%m-%d %H:%M:%S') + timedelta(**configs['interval'])
        ).replace(tzinfo=configs['timezone'])
    #End


    #Evaluating end point for interval
    d = dt.today() - timedelta(**configs['interval'])
    utc_to = dt(d.year,d.month,d.day,d.hour, d.minute,tzinfo=configs['timezone'])
    #End

    if utc_from < utc_to:
        # print('Updating {} from {} to {} ({})'.format(ticker,utc_from, utc_to, time_frame))

        del configs['timezone']
        del configs['time_frame']
        del configs['interval']
        
        configs |= dict(utc_from = utc_from, utc_to = utc_to, ticker = ticker)
        result = get_data(**configs)
        if result:
            if len(result) < 1:
                # print('Ticker: {} is up to date'.format(ticker))
                return None

        return result


    # print('Ticker: {} is up to date'.format(ticker))
    return





