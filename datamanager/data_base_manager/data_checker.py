"""
1. Checks if ticker in DB
2. Validates selected columns
3. Checks if data was uploaded correctrly
"""




def check_ticker(conn, ticker:str, time_frame:str) -> bool:

    #Checks if ticker is in DB

    ticker = f'{ticker}_{time_frame}'

    if ticker not in Tickers(conn):
        # raise Exception(f'{ticker} Ticker is not in the list')
        return False

    return True


def check_columns(conn, ticker:str, time_frame:str) -> bool:
    pass