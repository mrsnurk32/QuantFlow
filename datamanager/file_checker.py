"""
V 1.0
This module check the file system and creates files if missing
"""

import os

class DB_Checker:
    #checks for asset data in db

    @staticmethod
    def get_update(conn, ticker):

        """
            The function returns true if asset exists in db to initialize update
        if data is not present in db it will return false to initialize download method 
        """
            
        table_lst = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        table_lst = [i[0] for i in table_lst.fetchall() if i[0] != 'stock_info']
        table_lst = [i.split('_')[0] for i in table_lst if '1h' in i]

        if ticker in table_lst:
            return True

        else:
            return False
        


class FileCheck:

    """
    1. Checks for database directory
    2. Creates one if missing
    """
    
    DIRECTORIES = (
        'asset_data',
    )

    @property
    def check_files(self):

        file_list = os.listdir()
        for _dir in self.DIRECTORIES:
            if _dir not in file_list:
                print(f'created {_dir}')
                os.mkdir(_dir)
            



