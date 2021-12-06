from stocklab.simulation import *
from data.binance import read_binance_data
from strategies.midday import MidDayMulti
from stocklab.portfolio import Portfolio

coins = ["BAT", "ONE", "NEO", "TRX"]
portfolio = Portfolio()
dates = []
for coin in coins:
    df = read_binance_data(coin)
    dates = df["date"].values
    portfolio.add_symbol(coin, 1.0, df)

strategy = MidDayMulti(portfolio=portfolio)
sim = Simulation(1000, strategy, indexes=dates[:100])
while True:
    if sim.execute:
        pass
    else:
        break
strategy.score()

