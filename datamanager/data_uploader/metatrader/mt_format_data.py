import pandas as pd

__all__ = ['format_data']

def format_data(data):

    rates_frame = pd.DataFrame(data)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    return rates_frame