import MetaTrader5 as mt5

import pytz
from datetime import datetime as dt
from datetime import timedelta

import pandas as pd

from .modules import AssetConfig
from .modules import WeekDays

import asyncio

import time 


class DownloadAsset(AssetConfig):
    

    async def download(self,ticker, mt_t_frame, utc_from, rows):

        return mt5.copy_rates_from(ticker, mt_t_frame, utc_from, rows)

    
    async def download_mt_asset(self,ticker, time_frame, conn, rows = 50000):

        frame_header, mt_t_frame,\
            timezone = self.time_frame(time_frame)
            
        ymd = dt.today()
        
        if WeekDays.trading_day():

           delta = timedelta(days = 1)
           ymd = (ymd - delta)

        utc_from = dt(ymd.year, ymd.month, ymd.day, tzinfo=timezone)
       
        rates = await self.download(ticker, mt_t_frame, utc_from, rows)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

        if len(rates_frame) < 1:
            return "Check frame data ticker:{}".format(ticker)
       
        ticker = ticker + '_' + frame_header
        
        rates_frame.to_sql(name=ticker,con = conn,index=False)
        print(f'Downloaded {ticker} ({time_frame})')


class VerifyData(DownloadAsset):

    def verify_data(self,ticker, time_frame, rows = 500):

        frame_header, mt_t_frame,\
        timezone = self.time_frame(time_frame)
            
        ymd = dt.today()
        
        if WeekDays.trading_day():

           delta = timedelta(days = 1)
           ymd = (ymd - delta)

        utc_from = dt(ymd.year, ymd.month, ymd.day, tzinfo=timezone)
       
        rates = mt5.copy_rates_from(ticker, mt_t_frame, utc_from, rows)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

        if len(rates_frame) < 1:
            return "Check frame data ticker:{}".format(ticker)

        return rates_frame
