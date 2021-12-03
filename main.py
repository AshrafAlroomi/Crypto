from stocklab.simulation import *
from data import read_binance_data
from strategies.midday import MidDayMulti
from stocklab.portfolio import Portfolio

coins = ["BAT", "ONE", "NEO", "TRX"]
portfolio = Portfolio()
for coin in coins:
    df = read_binance_data(coin)
    dates = df["date"].values
    portfolio.add_symbol(coin, 1.0, df)

strategy = MidDayMulti(portfolio=portfolio, dates=dates)
sim = Simulation(1000, strategy)
sim.by_date()
strategy.score()
"""
path = "data/Binance_ONEUSDT_1h.csv"
df = read_binance_data(path)
strategy = MidDay(row_data=df)
strategy.MID_DAY = 5
strategy.STOP_LOSS = -0.02
strategy.TAKE_PROFIT = 0.03
sim = Simulation(1000, strategy)
sim.row_by_row()
strategy.score()
"""
