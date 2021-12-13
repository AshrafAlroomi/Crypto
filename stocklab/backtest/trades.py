import pandas as pd

from stocklab.vars import ORDERS


class Trade:
    def __init__(self, index, trade_type=ORDERS.buy):
        self.index = index
        self.order = None
        self.state = None
        self.profit = 0.0
        self.trade_type = trade_type

    def new(self, state, order):
        self.state = state
        self.order = order

        if self.trade_type == ORDERS.buy:
            # update balance after buy
            # TODO
            # the balance could be < 0
            self.state.balance -= self.state.strategy.buy_fees(self.order.hold.cost)

        elif self.trade_type == ORDERS.sell:

            # calculate cost of trade
            # calculate the profit after sell
            # with fees
            order_cost = self.order.hold.quantity * self.order.price
            released = self.state.strategy.sell_fees(order_cost)
            self.profit = released - self.order.hold.cost
            self.state.balance += released

        else:
            raise ValueError

    def __str__(self):
        return str(self.to_dict)

    @staticmethod
    def format_decimal(value):
        formatted_string = "{:.2f}".format(value)
        return float(formatted_string)

    @property
    def to_dict(self):
        if self.trade_type == ORDERS.sell:
            return {"score": self.format_decimal(self.order.score),
                    "name": self.order.hold.symbol.name,
                    "order": ORDERS.sell,
                    "price": self.order.hold.unit_price,
                    "quantity": self.order.hold.quantity,
                    "balance": self.format_decimal(self.state.balance),
                    "assets": self.format_decimal(self.state.get_assets),
                    "profit": self.format_decimal(self.profit)}

        elif self.trade_type == ORDERS.buy:
            return {"score": self.format_decimal(self.order.score),
                    "name": self.order.symbol.name,
                    "order": ORDERS.buy,
                    "price": self.order.price,
                    "quantity": self.order.hold.quantity,
                    "balance": self.format_decimal(self.state.balance),
                    "assets": self.format_decimal(self.state.get_assets),
                    "profit": 0.0}
        else:
            raise ValueError


class Trades:
    def __init__(self, trades=None):
        if trades is None:
            trades = []
        self.TRADES = trades
        self.all_profit = 0.0
        self.all_profit_pct = 0.0

    def add(self, trade):
        self.TRADES.append(trade)
        self.all_profit += trade.profit

    def screen(self):
        pass

    def by_index(self, index):
        return [trade.to_dict for trade in self.TRADES if trade.index == index]

    @property
    def to_dict(self):
        return [trade.to_dict for trade in self.TRADES]

    @property
    def to_df(self):
        return pd.DataFrame([trade.to_dict for trade in self.TRADES])
