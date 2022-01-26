import pandas as pd
from stocklab.portfolio.symbols import Symbols, Symbol
from stocklab.vars import COLS


class Portfolio(object):
    df: pd.DataFrame
    symbols = Symbols()

    def add_symbol(self, name: str, pct: float, df: pd.DataFrame):
        s = Symbol(name=name, pct=pct, df=df)
        self.symbols.add(s)

    def get_price(self, name: str, date, col=COLS.high):
        for symbol in self.symbols.SYMBOLS:
            if symbol.name == name:
                return symbol.get_by_index(date, col)
        return False
