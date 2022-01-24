from dataclasses import dataclass
from stocklab.portfolio.symbols import Symbol
from stocklab.backtest.holds import Hold
from typing import Optional


@dataclass
class Order:
    op: str
    symbol: Symbol
    hold: Optional[Hold] = None
    price: float = 0.0
    score: float = 0.0

    def get_quantity(self, balance):
        return (balance * self.symbol.pct) // self.price


@dataclass
class Orders:
    def __post_init__(self):
        self.ORDERS = []

    def add_order(self, order):
        # add new order
        # based on score value
        if len(self.ORDERS) == 0:
            self.ORDERS.append(order)
        else:
            idx = len(self.ORDERS) - 1
            for i in range(len(self.ORDERS)):
                if self.ORDERS[i].score <= order.score:
                    idx = i
                    break
            self.ORDERS.insert(idx + 1, order)

    def __iter__(self):
        return self.ORDERS.__iter__()
