import MetaTrader5 as mt5
import pytz

class AssetConfig:

    '''
    V 2.1
    AssetConfig class sets time zone and return config for timeframe
    '''

    TIME_FRAMES = {
        'd1':mt5.TIMEFRAME_D1,
        '1h':mt5.TIMEFRAME_H1,
        'min5':mt5.TIMEFRAME_M5,
        'min1':mt5.TIMEFRAME_M1
    }

    TIME_INTERVAL = {
        '1h':{'hours':1},
        'd1':{'days':1},
        'min1':{'minutes':1},
        'min5':{'minutes':5}
    }

    def __init__(self):

        self.timezone = pytz.timezone("Etc/UTC")

    @property
    def time_frames(self):
        return self.TIME_FRAMES.keys()

    
    def get_upload_interval(self, time_frame):
        return self.TIME_INTERVAL[time_frame]


    def time_frame(self,time_frame, update = False):

        # assert time_frame not in self.TIME_FRAMES

        if update == False:
            return time_frame, self.TIME_FRAMES[time_frame], self.timezone

        else:

            return time_frame, self.TIME_FRAMES[time_frame], self.timezone,\
                self.get_upload_interval(time_frame)


