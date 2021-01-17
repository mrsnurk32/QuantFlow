import pandas as pd


__all__ = ['RussianStockTickers']


class RussianStockTickers:

    @property
    def custom_ticker_list(self):

        tickers = pd.read_csv('approved_tickers.csv')
        return tickers.tickers.values

    def rtc_index_lst(self):
        pass
