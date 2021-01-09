class ApprovedTickers:

    @staticmethod
    def approved_tickers():


        c = sql.connect(
            '{}/stock_data/fin_data.db'.format(os.getcwd().replace('\\','/'))).cursor()

        table_lst = c.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")

        table_lst = [i[0] for i in table_lst.fetchall() if i[0] != 'stock_info']

        approved = list()

        for ticker in table_lst:
            frame = mtr.get_frame(ticker,simple = False)
            if len(frame) < 10000:continue
            approved.append(ticker)

        confirmed = list()

        for ticker in approved:
            frame = mtr.quick_frame(mtr.connect_to_db(),ticker)
            if frame.real_volume.mean() > 10000:
                confirmed.append(ticker)

        pd.DataFrame({'tickers':confirmed}).to_csv('approved_tickers.csv',index = False)