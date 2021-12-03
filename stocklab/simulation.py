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
    HOLDS = []

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


class State:
    def __init__(self, balance, fees):
        self.fees = fees
        self.holds = Holds()
        self.balance = balance
        self.trades = []

    def sell(self, order):
        if self.can_sell:
            cost = order.hold.amount * order.price
            profit = cost - order.hold.cost
            self.balance += profit
            self.holds.drop(order.hold)

            trade = {
                "name": order.hold.symbol.name,
                "order": ORDERS.sell,
                "price": order.hold.unit_price,
                "amount": order.hold.amount,
                "balance": self.balance,
                "assets": self.get_assets,
                "profit": profit}

            print(trade)
            self.trades.append(trade)
            return trade
        return False

    def buy(self, order):
        if self.can_buy:
            amount = self.get_amount(order.symbol, order.price)
            if amount > 0:
                hold = Hold(order.symbol, amount, order.price)
                self.holds.add(hold)
                self.balance -= hold.cost
                trade = {
                    "name": order.symbol.name,
                    "order": ORDERS.buy,
                    "price": order.price,
                    "amount": hold.amount,
                    "balance": self.balance,
                    "assets": self.get_assets,
                    "profit": 0.0}
                print(trade)
                self.trades.append(trade)
                return True
        return False

    def profit_pct(self, symbol, price):
        hold = self.holds.get(symbol)
        return hold.amount * price - hold.cost

    def get_amount(self, symbol, price):
        sub_balance = self.balance * symbol.pct
        return sub_balance // price

    @property
    def get_assets(self):
        assets = 0
        for h in self.holds.HOLDS:
            assets += h.cost
        return assets + self.balance

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

    def log(self, op, price, amount):
        print_arg = f"{op}, {op} at= {price} | currant balance= {self.state.balance} | amount= {amount}"
        self.print_template(print_arg)

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
