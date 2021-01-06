"""
V 1.0
This module check the file system and creates files if missing
"""

import os

class DBChecker:
    #checks if database exists
    pass


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
            



