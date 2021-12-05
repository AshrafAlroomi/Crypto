import uuid
from stocklab.config import *
import pandas as pd
from stocklab.portfolio import Symbols
from stocklab.index import Index


class Hold:
    def __init__(self, symbol=None, quantity=0, price=0.0):
        self.symbol = symbol
        self.quantity = quantity
        self.unit_price = price
        self.cost = price * quantity

    def profit_pct(self, price):
        return self.quantity * price - self.cost


class Holds:
    def __init__(self, holds=None):
        if holds is None:
            holds = []
        self.HOLDS = holds

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
            hold_dict = {}
            hold_dict["symbol"] = hold.symbol.name
            hold_dict["cost"] = hold.cost
            hold_dict["quantity"] = hold.quantity
            hold_dict["price"] = hold.unit_price
            hold_list.append(hold_dict)
        return hold_list


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
            self.profit = self.state.strategy.sell_fees(order_cost - self.order.hold.cost)
            self.state.balance += self.state.strategy.sell_fees(order_cost)

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


class State:
    def __init__(self, balance, strategy):
        self.strategy = strategy
        self.balance = balance
        self.holds = Holds()
        self.trades = Trades()

    def sell(self, order, index):
        if self.can_sell:
            # del hold
            self.holds.drop(order.hold)
            # create trade
            trade = Trade(index, ORDERS.sell)
            trade.new(self, order)
            self.trades.add(trade)
            return True
        return False

    def buy(self, order, index):
        if self.can_buy:
            # get how many unit can buy
            quantity = order.get_quantity(self.balance)
            if quantity > 0:
                # create hold
                hold = Hold(order.symbol, quantity, order.price)
                self.holds.add(hold)
                # add hold to order obj
                order.hold = hold
                # create trade
                trade = Trade(index, ORDERS.buy)
                trade.new(self, order)
                self.trades.add(trade)
                return True
        return False

    @property
    def get_assets(self):
        assets = self.balance
        for h in self.holds.HOLDS:
            assets += h.cost
        return assets

    @property
    def can_buy(self):
        return True

    @property
    def can_sell(self):
        return True


class Simulation:
    def __init__(self, balance, strategy, indexes):
        self.strategy = strategy
        self.state = State(balance, strategy)
        self.index = Index(indexes)
        self.response = False

    @property
    def execute(self):
        self.index.next()
        if self.index.current is None:
            return False
        orders = self.strategy.decision(self.state, self.index.current)
        for order in orders:
            if order.op == ORDERS.sell:
                self.response = self.state.sell(order, self.index.current)
            elif order.op == ORDERS.buy:
                self.response = self.state.buy(order, self.index.current)
            else:
                self.response = False

        return True

    @property
    def get_json(self):
        if self.response:
            return {
                "date": str(self.index.current),
                "trades": self.state.trades.by_index(self.index.current),
                "holds": self.state.holds.to_dict,
                "balance": self.state.balance,
                "assets": self.state.get_assets,
                "profit": self.state.trades.all_profit,
            }
        return {}
