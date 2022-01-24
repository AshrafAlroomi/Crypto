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

    def __sub__(self, other):
        return set(self.SYMBOLS) - set(other)

    def __iter__(self):
        return self.SYMBOLS.__iter__()
