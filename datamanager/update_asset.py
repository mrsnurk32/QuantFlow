"""
V 1.0
Module updates existing assets in the db.
"""


import MetaTrader5 as mt5
import pytz
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

from datamanager.modules.asset_config import AssetConfig
from datamanager.modules.weekdays import WeekDays

import asyncio
import time 


class UpdateAsset(AssetConfig):


    async def update_mt_asset(self, ticker,time_frame, conn):


        frame_header, mt_t_frame,\
            timezone, interval = self.time_frame(time_frame, update = True)

        ticker_ = f'{ticker}_{time_frame}'

        querry = conn.execute(
                 'SELECT * FROM {} ORDER BY time DESC LIMIT 1;'.format(ticker_)
             ).fetchall()[0][0]


        utc_from = (
                dt.strptime(querry,'%Y-%m-%d %H:%M:%S') + timedelta(**interval)
            ).replace(tzinfo=timezone)


        d = dt.today() - timedelta(**interval)
        utc_to = dt(d.year,d.month,d.day,d.hour, d.minute,tzinfo=timezone)


        if utc_from > utc_to:
            print('Ticker: {} is up to date'.format(ticker))
            return None

        print('Updating {} from {} to {} ({})'.format(ticker,utc_from, utc_to, time_frame))



        rates = mt5.copy_rates_range(ticker, mt_t_frame, utc_from, utc_to)
        rates_frame = pd.DataFrame(rates)

        print(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        ticker = f'{ticker}_{time_frame}'



        rates_frame.to_sql(
            name=ticker, con=conn,
            if_exists='append', index=False)

        return True