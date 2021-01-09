"""

"""



class RiskManager:

    """
        This class accounts balance, stop loss and take profit
    """

    def __init__(self, stop_loss, take_profit, balance):

        self._stop_loss = stop_loss
        self._take_profit = take_profit
        self._balance = balance


    @property
    def stop_loss(self):
        return self._stop_loss


    @property
    def take_profit(self):
        return self._take_profit