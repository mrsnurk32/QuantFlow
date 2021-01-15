import MetaTrader5 as mt5
import pytz

__all__ = ['asset_config', 'time_frames']


class AssetConfig:

    '''
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

    
    def get_upload_interval(self, time_frame:str) -> dict:
        """
            The method returns time interval for datetime

            args:
                1. time_frame: a string type object, that indicates time frame of time series

            returns:
                1. dict with time interval {time_unit:n}
        """
        return self.TIME_INTERVAL[time_frame]


    def __call__(self,time_frame:str, update = False) -> dict:

        """
            This class method validates the time_frame, and returns parameters for 'update' and 'download' functions

            args:
                1. time_frame: a string type object, that indicates time frame of time series
                2. update: a boolean, that clarify wether the call method needs to return download config data or update config data

            
                if update is False, the class method returns config data needed for download function:
                    time_frame, mt.TIMEFRAME, timezone

                otherwise the class method returns config data needed for updated function:
                    time_frame, mt.TIMEFRAME, timezone, upload_interval
        """

        assert time_frame in self.TIME_FRAMES, 'Such time frame is not supported'

        result = dict(
            time_frame = time_frame, mt_time_frame = self.TIME_FRAMES[time_frame], timezone = self.timezone
        )

        if update:
            result |= {'interval':self.get_upload_interval(time_frame)}
                       
        return result
                


asset_config = AssetConfig()
time_frames = AssetConfig().time_frames