import datetime
import pandas as pd
from stocklab.config import COLS


class Symbol(object):
    def __init__(self, name, pct, df):
        self.name = name
        self.pct = pct
        self.df = df

    def get_by_date(self, date, col):
        row = self.df.loc[self.df[COLS.date] == date][col]
        if not row.empty:
            return row.iloc[-1]
        return False


class Symbols:
    def __init__(self, symbols=None):
        if symbols is None:
            symbols = []
        self.SYMBOLS = symbols

    def add(self, symbol):
        self.SYMBOLS.append(symbol)

    def get(self, name):
        for s in self.SYMBOLS:
            if s.name == name:
                return s
        raise f"no symbols {name}"

    def __sub__(self, other):
        return set(self.SYMBOLS) - set(other)

    def __iter__(self):
        return self.SYMBOLS.__iter__()


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
                return symbol.get_by_date(date, col)
        return False

