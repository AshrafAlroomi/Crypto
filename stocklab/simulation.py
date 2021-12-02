from stocklab.config import *
import pandas as pd


class State(object):
    def __init__(self, balance, fees):
        self.balance = balance
        self.fees = fees
        self.holds = {"amount": 0, "price": 0}
        self.trades = []
        self.current_price = 0.0

    def sell(self, price):
        if self.can_sell:
            self.current_price = price
            self.balance += self.holds["amount"] * self.current_price - self.fees
            amount = self.holds["amount"]
            profile = self.get_profit - self.fees
            self.holds["amount"] = 0
            self.holds["price"] = 0

            trade = {"order": ORDERS.sell,
                     "price": price,
                     "amount": amount,
                     "balance": self.balance,
                     "assets": self.get_assets,
                     "profit": profile}

            print(trade)
            self.trades.append(trade)
            return trade
        return False

    def buy(self, price):
        if self.can_buy:
            self.current_price = price
            amount = self.balance // self.current_price
            self.balance -= amount * self.current_price
            self.holds["amount"] = amount
            self.holds["price"] = price

            trade = {"order": ORDERS.buy,
                     "price": price,
                     "amount": amount,
                     "balance": self.balance,
                     "assets": self.get_assets,
                     "profit": self.get_profit}
            print(trade)
            self.trades.append(trade)
            return True
        return False

    def profit_pct(self, price):
        new_balance = self.holds["amount"] * price + self.balance
        prev_balance = self.holds["amount"] * self.holds["price"] + self.balance

        return (new_balance - self.fees - prev_balance) / prev_balance

    @property
    def get_profit(self):
        return self.current_price * self.holds["amount"] - self.holds["price"] * self.holds["amount"]

    @property
    def get_assets(self):
        if self.holds["amount"] == 0:
            return self.balance
        return (self.holds["amount"] * self.current_price) + self.balance

    @property
    def can_buy(self):
        if self.holds["amount"] == 0:
            return True
        return False

    @property
    def can_sell(self):
        if self.holds["amount"] > 0:
            return True
        return False


class Simulation:
    def __init__(self, balance, strategy):
        self.strategy = strategy
        self.state = State(balance, strategy.fees())
        self.logger = pd.DataFrame({})

    def log(self, op, price, amount):
        print_arg = f"{op}, {op} at= {price} | currant balance= {self.state.balance} | amount= {amount}"
        self.print_template(print_arg)

    def row_by_row(self):
        for _, row in self.strategy.df.iterrows():
            decision, price = self.strategy.decision(row, self.state)
            if decision == ORDERS.buy:
                self.state.buy(price)
            elif decision == ORDERS.sell:
                self.state.sell(price)
            else:
                # Hold
                pass

    @staticmethod
    def print_template(print_arg):
        print("-" * 10)
        print(print_arg)
        # time.sleep(1)
        print("-" * 10)
