from stocklab.portfolio.symbols import Symbols, Symbol
from stocklab.backtest.index import Index
from pydantic.dataclasses import dataclass
from typing import List


@dataclass
class Hold:
    symbol: Symbol
    quantity: int
    unit_price: float
    index_current: Index

    @property
    def cost(self):
        return self.unit_price * self.quantity

    def profit_pct(self, price):
        return (self.quantity * price - self.cost) / self.cost


@dataclass
class Holds:
    HOLDS: List[Hold]

    def add(self, hold):
        self.HOLDS.append(hold)

    def drop(self, hold):
        for i in range(len(self.HOLDS)):
            if self.HOLDS[i] == hold:
                self.HOLDS.pop(i)
                break

    def get(self, symbol):
        for h in self.HOLDS:
            if h.symbol == symbol:
                return h
        raise f"no hold for {symbol}"

    def get_symbols_list(self):
        if self.HOLDS:
            return self.symbols
        return []

    @property
    def symbols(self):
        s = Symbols()
        for hold in self.HOLDS:
            s.add(hold.symbol)
        return s

    @property
    def get_current_prices(self):
        h = {}
        for hold in self.HOLDS:
            h[hold.symbol] = hold.cost
        return h

    @property
    def to_dict(self):
        hold_list = []
        for hold in self.HOLDS:
            hold_dict = {"symbol": hold.symbol.name, "cost": hold.cost, "quantity": hold.quantity,
                         "price": hold.unit_price}
            hold_list.append(hold_dict)
        return hold_list
