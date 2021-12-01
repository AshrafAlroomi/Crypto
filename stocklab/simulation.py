import time

import matplotlib.pyplot as plt
import numpy as np
import uuid
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.linear_model import LinearRegression
from munch import DefaultMunch

"""
only for long positions 
one tik

"""

ORDERS = {
    "buy": "Buy",
    "sell": "Sell",
    "hold": "hold"
}
ORDERS = DefaultMunch.fromDict(ORDERS)


class Strategy(ABC):

    @abstractmethod
    def setup_data(self) -> pd.DataFrame: pass

    @abstractmethod
    def decision(self, *args, **kwargs) -> tuple: pass

    @abstractmethod
    def should_buy(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def should_sell(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def fees(self) -> float: pass


class MidDay(Strategy):
    """
    This strategy for single tik by hour
    start at the beginning of day
    depends on the LinearRegression angle and value
    for number of hours .
    """

    def __init__(self, *args, **kwargs):
        self.row_data = kwargs["row_data"]
        self.df = self.setup_data()

    def setup_data(self):
        df = self.row_data.copy(deep=True)
        df["Buy"] = 0
        init_idx = df[df.date.dt.hour == 0].iloc[0].name
        last_idx = df[df.date.dt.hour == 23].iloc[-1].name
        df = df.iloc[init_idx:last_idx + 1]
        for idx, row in df[df.date.dt.hour == 5].iterrows():
            prices = df.iloc[idx - 6:idx].close.values
            x = np.array(range(0, 6))
            intercept, coef = self.linear_reg(y=prices, x=x)
            if coef <= 0:
                df.loc[idx + 1, 'Buy'] = 1
        return df

    def decision(self, row, state):

        current_price = row["high"]
        profit = state.profit_pct(current_price)
        if self.should_buy(row):
            return ORDERS.buy, current_price
        if self.should_sell(profit):
            return ORDERS.sell, current_price
        return ORDERS.hold, current_price

    def should_buy(self, row) -> bool:
        if row["Buy"] == 1:
            return True
        return False

    def should_sell(self, profit) -> bool:
        # take profit
        if profit >= 0.04:
            return True
        # stop loss
        if profit <= -0.01:
            return True
        return False

    def fees(self) -> float:
        return 2.0

    @staticmethod
    def linear_reg(x, y):
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        return lr.intercept_, lr.coef_


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
