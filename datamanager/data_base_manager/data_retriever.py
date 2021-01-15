__all__ = ['Tickers']


class TickerList:
    
    """
        Retrieves ticker list from database, takes conn as parameter, which stands for db connection
    """


    def __call__(self, conn):
            
        table_lst = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")

        table_lst = [i[0] for i in table_lst.fetchall()]

        #Must return list of tickers that are located in DB
        return table_lst


Tickers = TickerList()
