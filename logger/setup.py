from data.binance import get_symbols, read_binance_data
from stocklab.backtest.simulation import Simulation
from stocklab.portfolio.portfolio import Portfolio
from strategies.period import PatternWithIndicators

symbols_dict = {k: v for k, v in enumerate(get_symbols()[::-1])}
balance = int(input("balance default(1000): ") or "1000")
print(symbols_dict)
n_symbols = int(input("#n default(4): ") or "4")
symbols = {}
for n in range(n_symbols):
    key = int(input(f"symbol key default({symbols_dict[n]}): ") or n)
    pct = float(input("pct 0.25: ") or 0.25)
    symbols[symbols_dict[key]] = pct

portfolio = Portfolio()
dates = []
for coin, pct in symbols.items():
    df = read_binance_data(coin)
    dates = df["date"].values
    portfolio.add_symbol(coin, pct, df)

strategy = PatternWithIndicators(portfolio=portfolio)
sim = Simulation(balance, strategy, (dates, "date"))
