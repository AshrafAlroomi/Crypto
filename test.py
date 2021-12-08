from stocklab.backtest.simulation import Simulation
from data.binance import read_binance_data
from strategies.patterns import PatternStrategy, PatternStrategyByhour
from strategies.tests import RandomStrategy
from stocklab.portfolio.portfolio import Portfolio

coins = ["BAT", "ONE", "NEO", "TRX"]
portfolio = Portfolio()
dates = []
for coin in coins:
    df = read_binance_data(coin)
    dates = df["date"].values
    portfolio.add_symbol(coin, 1.0, df)

strategy = PatternStrategyByhour(portfolio=portfolio)
sim = Simulation(1000, strategy, (dates, "date"))

while True:
    if sim.execute:
        # print(sim.get_json.get("trades"))
        if sim.get_json.get("profit"):
            print(sim.get_json.get("profit"))
            print(sim.get_json.get("period"))
    else:
        break
strategy.score()
