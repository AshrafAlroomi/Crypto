from stocklab.simulation import *
from utlis import read_binance_data
from strategies.midday import MidDay

path = "data/Binance_DASHUSDT_1h.csv"
df = read_binance_data(path)
strategy = MidDay(row_data=df)
sim = Simulation(1000, strategy)
sim.row_by_row()
