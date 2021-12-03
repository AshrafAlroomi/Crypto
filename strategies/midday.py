import random

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from stocklab.portfolio import Portfolio
from stocklab.strategy import Strategy
from stocklab.config import *
from stocklab.order import Order


class MidDay(Strategy):
    """
    This strategy for single tik by hour
    start at the beginning of day depends
    on the LinearRegression angle and value
    for number of hours .
    """

    STOP_LOSS = -0.02
    TAKE_PROFIT = 0.03
    MID_DAY = 5

    def __init__(self, *args, **kwargs):
        self.row_data = kwargs["row_data"]
        self.df = self.setup_data()
        self.state = None

    def setup_data(self):
        df = self.row_data.copy(deep=True)
        df["Buy"] = 0
        init_idx = df[df.date.dt.hour == 0].iloc[0].name
        last_idx = df[df.date.dt.hour == 23].iloc[-1].name
        df = df.iloc[init_idx:last_idx + 1]
        xs = self.MID_DAY + 1
        for idx, row in df[df.date.dt.hour == self.MID_DAY].iterrows():
            prices = df.iloc[idx - xs:idx].close.values
            x = np.array(range(0, xs))
            intercept, coef = self.linear_reg(y=prices, x=x)
            if coef <= 0.0:
                df.loc[idx + 1, 'Buy'] = 1
        return df

    def decision(self, row, state):
        self.state = state
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
        if profit >= self.TAKE_PROFIT:
            return True
        # stop loss
        if profit <= self.STOP_LOSS:
            return True
        return False

    def fees(self) -> float:
        return 1.0

    @staticmethod
    def linear_reg(x, y):
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        return lr.intercept_, lr.coef_


class MidDayMulti(Strategy):
    STOP_LOSS = -0.02
    TAKE_PROFIT = 0.03
    MID_DAY = 5

    def __init__(self, *args, **kwargs):
        self.price_index = COLS.high
        self.dates = kwargs["dates"]
        if "portfolio" in kwargs:
            self.portfolio = kwargs["portfolio"]
            self.setup_data()
            assert isinstance(self.portfolio, Portfolio)
        else:
            raise "portfolio is a must"

    def setup_data(self):
        for symbol in self.portfolio.symbols:
            symbol.df["Buy"] = random.randint(0, 1)

    def decision(self, state, date):
        orders = []
        for hold in state.holds.HOLDS:
            price = hold.symbol.get_by_date(date, self.price_index)
            if price:
                if self.should_sell(hold, price):
                    order = Order(op=ORDERS.sell, hold=hold, price=price)
                    orders.append(order)

        for symbol in self.portfolio.symbols - state.holds.HOLDS:
            if self.should_buy(symbol, date):
                price = symbol.get_by_date(date, self.price_index)
                if price:
                    order = Order(op=ORDERS.buy, symbol=symbol, price=price)
                    orders.append(order)
        return orders

    def should_buy(self, symbol, date) -> bool:
        row = symbol.get_by_date(date, "Buy")
        if row == 1:
            return True
        return False

    def should_sell(self, hold, price) -> bool:
        # take profit
        if hold.profit_pct(price) >= self.TAKE_PROFIT:
            return True
        # stop loss
        if hold.profit_pct(price) <= self.STOP_LOSS:
            return True
        return False

    def fees(self) -> float:
        return 1.0

    @staticmethod
    def linear_reg(x, y):
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        return lr.intercept_, lr.coef_
