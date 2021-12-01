import datetime
import pandas as pd
from stocklab.simulation import *


def to_date(date):
    # 2017-08-17 04-AM
    #
    try:
        return datetime.datetime.strptime(date, '%Y-%m-%d %I-%p')
    except:
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def read_data(tik):
    usd = 'USDT'
    time = '1h'
    name = f'Binance_{tik + usd}_{time}.csv'
    dfh = pd.read_csv(f'data/{name}', skiprows=1).iloc[::-1]
    dfh.head()
    dfh.reset_index(inplace=True, drop=True)
    dfh['date'] = dfh['date'].apply(lambda x: to_date(x))
    return dfh


strategy = MidDay(row_data=read_data('XRP'))
sim = Simulation(1000, strategy)
sim.row_by_row()
