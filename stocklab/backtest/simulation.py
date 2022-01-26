from stocklab.backtest.state import State
from stocklab.backtest.index import Index
from stocklab.strategy.abs import Strategy
from stocklab.vars import ORDERS
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Simulation:
    strategy: Strategy
    balance: int
    indexes: Tuple

    def __post_init__(self):
        self.response = False
        self.first_index = None
        self.state = State(balance=self.balance, strategy=self.strategy)
        self.index = Index(self.indexes[0], self.indexes[1])

    @property
    def execute(self):
        self.index.next()
        if self.index.current is None:
            return False
        if self.first_index is None:
            self.first_index = self.index.current
        orders = self.strategy.decision(state=self.state, index=self.index)
        for order in orders:
            if order.op == ORDERS.sell:
                self.response = self.state.sell(order, self.index)
            elif order.op == ORDERS.buy:
                self.response = self.state.buy(order, self.index)
            else:
                self.response = False

        return True

    @property
    def get_json(self):
        period = self.index.current - self.first_index
        return {
            "period": str(period.astype('timedelta64[D]')),
            "date": str(self.index.current),
            "trades": self.state.trades.by_index(self.index),
            "holds": self.state.holds.to_dict,
            "balance": self.state.balance,
            "assets": self.state.get_assets,
            "profit": self.state.trades.all_profit,
        }
