import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


class BackTester:
    
    def __init__(self, take_profit, stop_loss):
        
        #stop loss and take profit are expressed with integers ex. 1 = 1%
        self.take_profit = take_profit
        self.stop_loss = stop_loss


    def simple_backtest(self, frame):
        
        """
            The function back tests the strategy, the frame argument must contain Criteria column.
            Parameters such as stop loss and take profit are neglected.
            Strategy_returns column is returned once the fucntion is done.
        """

        initial_price = frame.close.iloc[0]
        frame['ret'] = frame.close.pct_change()    
        frame['Strategy_returns'] = initial_price * (1 + (frame['Criteria'].shift(1) * frame['ret'] )).cumprod()      
                        
        return frame

    def backtest(self, frame):

        """
            The function back tests the strategy, the frame argument must contain Criteria column.
            Parameters such as stop loss and take profit are being considered. The function takes longer to execute, but gives more
            accurate results. Strategy_returns column is returned once the fucntion is done.
        """

        # add feature that would account entry and exit points

        frame['ret'] = frame.close.pct_change()
        frame['Criteria_before'] = frame.Criteria.shift(1)
        
        stop_loss = self.stop_loss
        
        buy_trigger = False
        sell_trigger = True
        holding = False
        
        sl = None
        
        strategy_results = list()
        initial_price = frame.close.iloc[0]

        
        for row in frame.itertuples(index = False):
            
            if not holding:
                if row.Criteria and not row.Criteria_before:
                    buy_trigger = True
                    strategy_results.append(0)
                    continue
                
                elif buy_trigger:
                    buy_trigger = False
                    holding = True
                    sl = row.open * (1 - stop_loss)
                    strategy_results.append(row.ret)
                    continue
                    
                else:
                    strategy_results.append(0)
                
            
            else:
                if not row.Criteria and row.Criteria_before:
                    sell_trigger = True
                    strategy_results.append(row.ret)
                    continue
                    
                elif sell_trigger:
                    sell_trigger = False
                    holding = False
                    strategy_results.append(0)
                    sl = None
                    continue
                    
                elif row.low < sl:
                    holding = False
                    strategy_results.append(-stop_loss)
                    sl = None
                    continue
                    
                else:
                    strategy_results.append(row.ret)
                        
        frame['Strategy_results'] = strategy_results
        frame['Criteria_'] = np.where(pd.isna(frame["Strategy_results"]), False, True)
        frame['Strategy_returns'] = initial_price * (1 + (frame['Criteria_'].shift(1) * frame['Strategy_results'] )).cumprod()      

        
        del frame['Criteria_before']
        return frame
        
        

    @staticmethod
    def evaluate_strategy(frame):
    #required columns [close, ret]
    
        def get_data(df, year = None):
            
            if year is not None:
                df = df[df.time.dt.year == year].copy()
                
            return dict(
                strategy_net_income = df.Strategy_returns.iloc[-1] / df.Strategy_returns.iloc[0] -1,
                sharpe_ratio = (df.ret.mean() / df.ret.std())*np.sqrt(len(df)),
                max_drop_down = (df.Strategy_returns.min() / df.Strategy_returns.iloc[0]) - 1,
                asset_net_income = df.close.iloc[-1] / df.close.iloc[0] - 1,
                asset_peak = df.close.max() / df.close.iloc[0] -1,
                asset_min = df.close.min() / df.close.iloc[0] -1
            )
       
        frame = frame.iloc[1:]
        total_result = get_data(df = frame)
        
        year_list = frame.time.dt.year.unique()


        compare_list = list(map(lambda year:get_data(df = frame, year = year),year_list))
        
        return pd.DataFrame(compare_list , index = year_list)
            
        
    @staticmethod
    def visualize(frame, cols):


        """
            Visualize strategy, required columns in data frame are: close, Strategy_returns.
        Indicator columns can be added as well.

        """
        
        plt.rcParams["figure.figsize"] = [20, 10]
        return frame[cols].plot(grid=True, kind='line', title="Strategy vs Buy & Hold", logy=True)

