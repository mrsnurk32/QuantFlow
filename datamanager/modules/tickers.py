import pandas as pd
from os.path import join, dirname, abspath


__all__ = ['approved_tickers']


class RussianStockTickers:

    def __init__(self):
        self.approved_tickers_path = join(dirname(dirname(abspath(__file__))), 'data_uploader/approved_tickers.csv')

    @property
    def get_tickers(self):

        tickers = pd.read_csv(self.approved_tickers_path)
        return tickers.tickers.values


approved_tickers = RussianStockTickers().get_tickers