__all__ = ['commit_handler']

class MT_CommitHandler:

    def __handle_commit(self, conn, frame, ticker):
        frame.to_sql(name=ticker,con = conn,index=False)
        print(ticker, ': was downloaded')
        return True


    def __commit_update(self, conn, frame, ticker):
        frame.to_sql(name=ticker, con=conn, if_exists='append', index=False)
        print(ticker, ': was updated')
        return True
        
    
    def __call__(self, conn, frame, ticker, update=True):
        if update:
            self.__commit_update(conn, frame, ticker)
            return True
        
        else:
            self.__commit_download(conn, frame, ticker)
            return True
            


commit_handler = MT_CommitHandler()