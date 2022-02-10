import os
import requests
from binance import get_symbols


# ref : https://www.cryptodatadownload.com/data/binance/

def get_link(coin, usd='USDT', time='1h'):
    if time == 'Daily':
        time = 'd'
    elif time == 'Minute':
        time = 'minute'
    else:
        time = '1h'
    return f"https://www.cryptodatadownload.com/cdd/Binance_{coin + usd}_{time}.csv"


if __name__ == '__main__':

    for coin in get_symbols():
        for t in ['Daily', 'Hourly']:
            try:
                endpoint = get_link(coin=coin, time=t)
                file_name = endpoint.split('/')[-1]
                if not os.path.isdir('dfs'):
                    os.mkdir("dfs")
                if file_name in os.listdir('dfs'):
                    continue
                response = requests.get(endpoint, verify=False)
                with open('dfs/' + file_name, 'wb') as f:
                    f.write(response.content)
                    print("Done")
            except Exception as e:
                print(e)
