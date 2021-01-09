class QuantMetrics:

    # class Returns:
        
    #     @staticmethod
    #     def returns(frame):
    #         pass
        

    #     @staticmethod
    #     def future_returns(frame, period):
    #         pass


    # class SimpleMovingAverage:

    #     PERIODS = (12,24,48,100,200)

    #     @staticmethod
    #     def sma(frame, period):

    #         frame[f'SMA_{period}'] = df.close.rolling(ma).mean()
    #         return df


    # class StandardDeviation:

    #     @staticmethod
    #     def standard_deviation(frame, period):
 
    #         if 'Returns' not in df.columns:df = self.returns(df)
    #         df['STD{}'.format(std)] = temp.Return.rolling(std).std()

    #         return df


    # class Stochastic:
        
    #     @staticmethod
    #     def stochastic(frame):
        
    #         frame['Min'] = frame.low.rolling(14).min()
    #         frame['close-min'] = frame.close - frame.Min
    #         frame['H-L'] = frame.high.rolling(14).max() - frame.low.rolling(14).min()
    #         frame['K'] = frame['close-min'] / frame['H-L'] * 100
    #         frame['SlowK'] = (frame['close-min'].rolling(3).sum() / frame['H-L'].rolling(3).sum()) * 100
    #         return frame


    class MACD:

        @staticmethod
        def macd(frame):

            frame['EMA12'] = frame.close.ewm(span=12).mean()
            frame['EMA26'] = frame.close.ewm(span=26).mean()
            frame['Difference'] = frame.EMA12 - frame.EMA26
            frame['Signal'] = frame.Difference.ewm(span=9).mean() #9 period ema
            frame['Histogram'] = frame.Difference - frame.Signal
            return frame


    # class Slope:

    #     @staticmethod
    #     def slope(frame):

    #         frame['slope_25'] = (frame.close - frame.close.shift(25)) / 25
    #         frame['slope_12'] = (frame.close - frame.close.shift(12)) / 12

    #         return frame


class QuantMethods(QuantMetrics):

    def macd(self, frame):
        return self.MACD.macd(frame)       


quant_metrics = QuantMethods()
        


    