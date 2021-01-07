"""
V 1.0
1. The class RussianStock Tickers gets ticker list of Russian Index RTC
"""


import pandas as pd
import wikipedia as wp


class RussianStockTickers:

    @property
    def get_tickers(self):

        html = wp.page("Индекс РТС").html().encode("UTF-8")

        try:
            df = pd.read_html(html)[1]

        except IndexError:
            df = pd.read_html(html)[0]

        df = df.iloc[1:]

        return df[1].values