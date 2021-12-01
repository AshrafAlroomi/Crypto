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
    def decision(self, *args, **kwargs) -> str: pass

    @abstractmethod
    def should_buy(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def should_sell(self, *args, **kwargs) -> bool: pass


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
        self.profit = 0
        self.current_price = 0

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

    def decision(self, row, state, current_price):

        self.current_price = current_price
        self.profit = state.cal_profit(current_price)
        if self.should_buy(row):
            return ORDERS.buy
        if self.should_sell(row):
            return ORDERS.sell
        return ORDERS.hold

    def should_buy(self, row) -> bool:
        if row["Buy"] == 1:
            return True
        return False

    def should_sell(self, row) -> bool:
        # take profit
        if self.profit >= 0.01:
            print("take profit")
            print(self.profit)
            return True
        # stop loss
        if self.profit <= -0.01:
            print("stop loss")
            print(self.profit)
            return True
        return False

    @staticmethod
    def linear_reg(x, y):
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        return lr.intercept_, lr.coef_


class State(object):
    def __init__(self, balance):
        self.balance = balance
        self.holds = {"amount": 0, "price": 0}

    def update_buy(self, price):
        amount = self.balance // price
        self.balance -= amount * price
        self.holds["amount"] = amount
        self.holds["price"] = price

    def update_sell(self, price):
        self.balance += self.holds["amount"] * price
        profit = self.cal_profit(price)
        self.holds["amount"] = 0
        self.holds["price"] = 0
        return profit

    def cal_profit(self, price):
        return price * self.holds["amount"] - self.holds["price"] * self.holds["amount"]

    def cal_assets(self, price):
        if self.holds["amount"] == 0:
            return self.balance
        return (self.holds["amount"] * price) + self.balance

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
        self.state = State(balance)
        self.logger = pd.DataFrame({})

    def buy(self, price):
        if self.state.can_buy:
            self.state.update_buy(price)
            self.log("buy", price, self.state.holds["amount"])

    def sell(self, price):
        if self.state.can_sell:
            amount = self.state.holds["amount"]
            self.state.update_sell(price)
            self.log("sell", price, amount)
        else:
            print("pass sell")
            pass

    def log(self, op, price, amount):
        print_arg = f"{op}, {op} at= {price} | currant balance= {self.state.balance} | amount= {amount}"
        self.print_template(print_arg)

    def row_by_row(self):
        for _, row in self.strategy.df.iterrows():
            price = row["high"]
            decision = self.strategy.decision(row, self.state, price)

            if decision == ORDERS.buy:
                self.buy(price)
            elif decision == ORDERS.sell:
                self.sell(price)
            else:
                # Hold
                pass

    @staticmethod
    def print_template(print_arg):
        print("-" * 10)
        print(print_arg)
        # time.sleep(1)
        print("-" * 10)
