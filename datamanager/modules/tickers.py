"""
V 1.0
1. The class RussianStock Tickers gets ticker list of Russian Index RTC
"""


import pandas as pd



class RussianStockTickers:

    @property
    def get_tickers(self):

        tickers = pd.read_csv('approved_tickers.csv')
        return tickers.tickers.values
