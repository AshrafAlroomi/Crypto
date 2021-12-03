from stocklab.simulation import *
from utlis import read_binance_data
from strategies.midday import MidDayMulti
from stocklab.portfolio import Portfolio

tiks = ["AAVE", "ONE"]
portfolio = Portfolio()
for tik in tiks:
    path = f"data/Binance_{tik}USDT_1h.csv"
    df = read_binance_data(path)
    dates = df["date"].values
    portfolio.add_symbol(tik, 0.5, df)

strategy = MidDayMulti(portfolio=portfolio, dates=dates)
sim = Simulation(100, strategy)
sim.by_date()
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
