import pandas as pd
import numpy as np
from ..metrics import quant_metrics



class MACD_Simple:

    '''
        Simple MACD strategy, tells bot to buy when EMA12 > EMA26
    '''
    
    @staticmethod
    def get_strategy_frame(frame):
        
        quant_metrics.macd(frame)
        frame['MA_100'] = frame.close.rolling(100).mean()
        frame['Criteria'] = np.where(
            (frame['EMA12'] > frame['EMA26']) & (frame.close > frame['MA_100']), True,False
        )
        return frame


def macd_simple(frame):
    return MACD_Simple.get_strategy_frame(frame)