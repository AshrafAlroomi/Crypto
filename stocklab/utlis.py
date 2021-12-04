import pandas as pd
import datetime


class CryptoData(object):
    # TODO
    def __init__(self, *args, **kwargs):
        if kwargs["path"]:
            if isinstance(kwargs["path"], list):
                pass
            elif isinstance(kwargs["path"], str):
                self.path = [kwargs["path"]]
            else:
                raise Exception

    def binance_data(self):
        def to_date(date):
            try:
                return datetime.datetime.strptime(date, '%Y-%m-%d %I-%p')
            except:
                return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        for path in self.path:
            df = pd.read_csv(path, skiprows=1).iloc[::-1]
            df.reset_index(inplace=True, drop=True)
            df['date'] = df['date'].apply(lambda x: to_date(x))
            return df





