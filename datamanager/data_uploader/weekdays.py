"""
V 1.0
WeekDays class return true if today is a weekday
"""

import datetime as dt


class WeekDays:

    #returns whether it`s a weekend or not

    @staticmethod
    def trading_day():

        #Return true if its weekday, doesn`t account national holidays
        weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        weekDay = weekDays[dt.date.today().weekday()]

        today = dt.date.today().strftime('%Y.%m.%d')
        hour = dt.datetime.now().hour
        
        work_time = range(9,19)
        
        if weekDay in weekDays[-2:] or hour not in work_time:
            
            return False

        else:
    
            return True
            

class Russia(WeekDays):
    pass


class USA(WeekDays):
    pass


if __name__ == '__main__':

    print(WeekDays.trading_day())