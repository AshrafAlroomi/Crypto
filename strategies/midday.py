import numpy as np
from sklearn.linear_model import LinearRegression
from stocklab.strategy import Strategy
from stocklab.config import *


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
        return 0.0

    @staticmethod
    def linear_reg(x, y):
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        return lr.intercept_, lr.coef_
