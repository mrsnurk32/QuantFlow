import MetaTrader5 as mt5
import pytz

class AssetConfig:

    '''
    AssetConfig class sets time zone and return config for timeframe
    '''

    TIME_FRAMES = {
        'd1':mt5.TIMEFRAME_D1,
        '1h':mt5.TIMEFRAME_H1,
        'min5':mt5.TIMEFRAME_M5
    }

    def __init__(self):

        self.timezone = pytz.timezone("Etc/UTC")


    def time_frame(self,time_frame):

        # assert time_frame not in self.TIME_FRAMES
        return time_frame, self.TIME_FRAMES[time_frame], self.timezone
