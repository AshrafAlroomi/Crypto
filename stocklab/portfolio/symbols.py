import pandas as pd
from typing import List
from dataclasses import dataclass


@dataclass
class Symbol(object):
    name: str
    pct: float
    df: pd.DataFrame

    def get_by_index(self, index, col: str):
        row = self.df.loc[self.df[index.col_name] == index.current][col]
        if not row.empty:
            return row.iloc[-1]
        return False


@dataclass
class Symbols:

    def __post_init__(self):
        self.SYMBOLS = []

    def add(self, symbol: Symbol):
        self.SYMBOLS.append(symbol)

    def get(self, name: str):
        for s in self.SYMBOLS:
            if s.name == name:
                return s
        raise f"no symbols {name}"

    @property
    def names(self):
        return [x.name for x in self.SYMBOLS]

    def __sub__(self, other):
        l = other.SYMBOLS
        for s in self.SYMBOLS:
            if s.name in other.names:
                l.remove(s)
            else:
                l.append(s)
        return l

        return 0
        # for s in self.SYMBOLS:
        #     if s
        #
        # return [x if x not in other.SYMBOLS for x in self.SYMBOLS]
        # return set(self.SYMBOLS) - set(other.SYMBOLS)

    def __iter__(self):
        return self.SYMBOLS.__iter__()
