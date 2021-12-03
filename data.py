import requests
import os
import datetime
import pandas as pd


def get_coin_path(coin, usd='USDT', time='1h'):
    if time == 'Daily':
        time = 'd'
    elif time == 'Minute':
        time = 'minute'
    else:
        time = '1h'
    return f"data/Binance_{coin}{usd}_{time}.csv"


def download_data():
    # ref : https://www.cryptodatadownload.com/data/binance/
    def get_link(coin, usd='USDT', time='1h'):
        if time == 'Daily':
            time = 'd'
        elif time == 'Minute':
            time = 'minute'
        else:
            time = '1h'
        return f"https://www.cryptodatadownload.com/cdd/Binance_{coin + usd}_{time}.csv"

    for coin in get_symbols():
        for t in ['Daily', 'Hourly']:
            try:
                endpoint = get_link(coin=coin, time=t)
                file_name = endpoint.split('/')[-1]
                if file_name in os.listdir('./data'):
                    continue
                response = requests.get(endpoint, verify=False)
                with open('data/' + file_name, 'wb') as f:
                    f.write(response.content)
            except Exception as e:
                print(e)


def get_symbols():
    # ref : https://www.cryptodatadownload.com/data/binance/
    data_string = """BTC/USDT [Daily] [Hourly] [Minute] ... [Value at Risk]
    ETH/USDT [Daily] [Hourly] [Minute] ... [Value at Risk]
    LTC/USDT [Daily] [Hourly] [Minute] ... [Value at Risk]
    NEO/USDT [Daily] [Hourly] [Minute]
    BNB/USDT [Daily] [Hourly] [Minute]
    XRP/USDT [Daily] [Hourly] [Minute]
    LINK/USDT [Daily] [Hourly] [Minute]
    EOS/USDT [Daily] [Hourly] [Minute]
    TRX/USDT [Daily] [Hourly] [Minute]
    ETC/USDT [Daily] [Hourly] [Minute]
    XLM/USDT [Daily] [Hourly] [Minute]
    ZEC/USDT [Daily] [Hourly] [Minute]
    ADA/USDT [Daily] [Hourly] [Minute]
    QTUM/USDT [Daily] [Hourly] [Minute]
    DASH/USDT [Daily] [Hourly] [Minute]
    XMR/USDT [Daily] [Hourly] [Minute]
    BAT/USDT [Daily] [Hourly] [Minute]
    BTT/USDT [Daily] [Hourly] [Minute]
    ZEC/USDT [Daily] [Hourly] [Minute]
    USDC/USDT [Daily] [Hourly] [Minute]
    TUSD/USDT [Daily] [Hourly] [Minute]
    MATIC/USDT [Daily] [Hourly] [Minute]
    PAX/USDT [Daily] [Hourly] [Minute]
    CELR/USDT [Daily] [Hourly] [Minute]
    ONE/USDT [Daily] [Hourly] [Minute]
    DOT/USDT [Daily] [Hourly] [Minute]
    UNI/USDT [Daily] [Hourly] [Minute]
    ICP/USDT [Daily] [Hourly] [Minute]
    SOL/USDT [Daily] [Hourly] [Minute]
    VET/USDT [Daily] [Hourly] [Minute]
    FIL/USDT [Daily] [Hourly] [Minute]
    AAVE/USDT [Daily] [Hourly] [Minute]
    DAI/USDT [Daily] [Hourly] [Minute]
    MKR/USDT [Daily] [Hourly] [Minute]
    ICX/USDT [Daily] [Hourly] [Minute]
    CVC/USDT [Daily] [Hourly] [Minute]
    SC/USDT [Daily] [Hourly] [Minute]
    LRC/USDT [Daily] [Hourly] [Minute]"""

    return [x.split('/')[0] for x in data_string.split('\n')]


def read_binance_data(coin):
    def to_date(date):
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d %I-%p')
        except:
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    path = get_coin_path(coin)
    df = pd.read_csv(path, skiprows=1).iloc[::-1]
    df.reset_index(inplace=True, drop=True)
    df['date'] = df['date'].apply(lambda x: to_date(x))
    return df
