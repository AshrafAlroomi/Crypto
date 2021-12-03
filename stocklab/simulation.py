import uuid
from stocklab.config import *
import pandas as pd
from stocklab.portfolio import Symbols


class Hold:
    def __init__(self, symbol=None, amount=0, price=0.0):
        self.symbol = symbol
        self.amount = amount
        self.unit_price = price
        self.cost = price * amount

    def profit_pct(self, price):
        return self.amount * price - self.cost


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


class Trade:
    def __init__(self, trade_type=ORDERS.buy):
        self.id = uuid.uuid1().hex[:6]
        self.order = None
        self.state = None
        self.profit = 0.0
        self.trade_type = trade_type

    def new(self, state, order):
        self.state = state
        self.order = order

        if self.trade_type == ORDERS.buy:
            # update balance after buy
            self.state.balance -= self.order.hold.cost

        elif self.trade_type == ORDERS.sell:

            # calculate cost of trade
            # calculate the profit after sell
            order_cost = self.order.hold.amount * self.order.price
            self.profit = order_cost - self.order.hold.cost
            self.state.balance += order_cost

        else:
            raise ValueError

    def __str__(self):
        return self.to_dict

    @property
    def to_dict(self):
        if self.trade_type == ORDERS.sell:
            return {"score": self.order.score,
                    "name": self.order.hold.symbol.name,
                    "order": ORDERS.sell,
                    "price": self.order.hold.unit_price,
                    "amount": self.order.hold.amount,
                    "balance": self.state.balance,
                    "assets": self.state.get_assets,
                    "profit": self.profit}

        elif self.trade_type == ORDERS.buy:
            return {"score": self.order.score,
                    "name": self.order.symbol.name,
                    "order": ORDERS.buy,
                    "price": self.order.price,
                    "amount": self.order.hold.amount,
                    "balance": self.state.balance,
                    "assets": self.state.get_assets,
                    "profit": 0.0}
        else:
            raise NotImplementedError


class Trades:
    def __init__(self, trades=None):
        if trades is None:
            trades = []
        self.TRADES = trades

    def add(self, trade):
        self.TRADES.append(trade)

    def screen(self):
        pass

    def by_id(self, trade_id):
        for trade in self.TRADES:
            if trade.id == trade_id:
                return trade
        return False

    def by_order(self, order):
        for trade in self.TRADES:
            if trade.order == order:
                return trade
        return False

    def by_hold(self, hold):
        for trade in self.TRADES:
            if trade.hold == hold:
                return trade
        return False

    @property
    def to_df(self):
        return pd.DataFrame([trade.to_dict for trade in self.TRADES])


class State:
    def __init__(self, balance, fees):
        self.fees = fees
        self.balance = balance
        self.holds = Holds()
        self.trades = Trades()

    def sell(self, order):
        if self.can_sell:
            # del hold
            self.holds.drop(order.hold)
            # create trade
            trade = Trade(ORDERS.sell)
            trade.new(self, order)
            print(trade)
            self.trades.add(trade)
            return True
        return False

    def buy(self, order):
        if self.can_buy:
            # get how many unit can buy
            amount = order.get_amount(self.balance)
            if amount > 0:
                # create hold
                hold = Hold(order.symbol, amount, order.price)
                self.holds.add(hold)
                # add hold to order obj
                order.hold = hold
                # create trade
                trade = Trade(ORDERS.buy)
                trade.new(self, order)
                print(trade)
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
    def __init__(self, balance, strategy, price_index="high"):
        self.strategy = strategy
        self.price_index = price_index
        self.state = State(balance, strategy.fees())
        self.logger = pd.DataFrame({})

    def by_row(self):
        for _, row in self.strategy.df.iterrows():
            orders = self.strategy.decision(self.state, row)
            for order in orders:
                if order.op == ORDERS.sell:
                    self.state.sell(order)
                elif order.op == ORDERS.buy:
                    self.state.buy(order)

    def by_date(self):
        for date in self.strategy.dates:
            print('-' * 10)
            orders = self.strategy.decision(self.state, date)
            for order in orders:
                if order.op == ORDERS.sell:
                    self.state.sell(order)
                elif order.op == ORDERS.buy:
                    self.state.buy(order)

    @staticmethod
    def print_template(print_arg):
        print("-" * 10)
        print(print_arg)
        # time.sleep(1)
        print("-" * 10)
