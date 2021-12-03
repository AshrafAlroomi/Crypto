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
    SYMBOLS = []

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

    """
    def add_symbol(self, symbol, pct, df):
        new_naming = {col: f"{col}_{symbol}" for col in df.columns if col != COLS.date}
        df.rename(new_naming, axis=1, inplace=True)
        df.set_index([COLS.date], inplace=True)
        if self.df.empty:
            self.df = df
        else:
            pd.concat([self.df, df], axis=1)
        s = Symbol(name=symbol, pct=pct)
        self.symbols.add(s)

    def get_symbol(self, idx):
        s = idx.split("_")[-1]
        return self.symbols.get(s)

    def set_current_symbol(self, name):
        self.sy = self.symbols.get(name)
        return self.sy

    def s_available_in_date(self, date):
        if not self.sy:
            raise "use set_current_symbol"
        assert isinstance(date, datetime.datetime)
        if self.df[self.df[COLS.date] == date].empty:
            return False
        return True

    def row_in_date(self, date):
        if not self.sy:
            raise "use set_current_symbol"
        assert isinstance(date, datetime.datetime)
        row = self.df[self.df[COLS.date] == date]
        if row.empty:
            return False
        return row

    def get_price(self, symbol, date):
        self.c
        row = self.row_in_date(date)
    """
