import pandas as pd
from stocklab.portfolio.symbols import Symbols, Symbol
from stocklab.vars import COLS


class Portfolio(object):
    def __init__(self):
        self.df = pd.DataFrame()
        self.symbols = Symbols()
        self.sy = None

    def add_symbol(self, name, pct, df):
        s = Symbol(name=name, pct=pct, df=df)
        self.symbols.add(s)

    def get_price(self, name, date, col=COLS.high):
        for symbol in self.symbols.SYMBOLS:
            if symbol.name == name:
                return symbol.get_by_index(date, col)
        return False
