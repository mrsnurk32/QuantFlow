


"""
V 1.0
Establishes DB connection
"""


class Connector:
    #The class establishes connection with DB.

    def connect_to_db(self):

        db_file_path = 'stock_data/fin_data.db'.format()
        sqlite3_conn = None

        try:

            sqlite3_conn = sql.connect(db_file_path)
            return sqlite3_conn
        
        except Error as err:

            print(err)
            if sqlite3_conn is not None:
                sqlite3_conn.close()