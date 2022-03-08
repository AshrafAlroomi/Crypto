import sys
from data.binance import get_symbols, read_binance_data
from stocklab.backtest.simulation import Simulation
from stocklab.portfolio.portfolio import Portfolio
from strategies.period import PatternWithIndicators
from strategies.sandr import SRStrategy

method = None
if len(sys.argv) > 1:
    method = sys.argv[1]

if method is None:
    balance = 1000
    coins = {0: 'LRC', 1: 'SC', 2: 'CVC', 3: 'ICX'}
    portfolio = Portfolio()
    for _, coin in coins.items():
        df = read_binance_data(coin)
        dates = df["date"].values
        portfolio.add_symbol(coin, 0.25, df)
    strategy = SRStrategy(portfolio=portfolio)
    sim = Simulation(balance=balance, strategy=strategy, indexes=(dates, "date"))

elif method == "user":
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

    strategy = SRStrategy(portfolio=portfolio)
    sim = Simulation(balance=balance, strategy=strategy, indexes=(dates, "date"))
elif method == "all":
    balance = 1000
    coins = get_symbols()
    portfolio = Portfolio()
    for coin in coins:
        df = read_binance_data(coin)
        dates = df["date"].values
        portfolio.add_symbol(coin, 0.25, df)
    strategy = SRStrategy(portfolio=portfolio)
    sim = Simulation(balance=balance, strategy=strategy, indexes=(dates, "date"))
