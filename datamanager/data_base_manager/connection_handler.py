import sqlite3 as sql
from os.path import join, dirname, abspath

__all__ = ['Connector', 'MT_MOEX_Stocks']

class Connector:
    
    """
    1. Establishes connection with db
    2. Closes connection with db
    """
    
    def __init__(self, directory):
        self.directory = directory


    def __enter__(self):

        """
            This method checks if db inplace

            returns:
                connection to db
        """

        # FileCheck().check_files

        self.conn = sql.connect(self.directory)
        return self.conn
        
    def __exit__(self,exc_type,exc_value, exc_tb):

        """
            This method aborts connection with db
        """

        if self.conn:
            self.conn.close()


class Directrory:

    """
        This class returns path to db
    """

    @property
    def get_path(self):
        return self.directory



class MT_MOEX_Stocks(Directrory):

    """
        This class stores db path
    """

    def __init__(self):
        self.directory = join(dirname(dirname(dirname(abspath(__file__)))), 'asset_data\stock_data.db')
