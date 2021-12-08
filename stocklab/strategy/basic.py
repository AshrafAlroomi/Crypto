import random

import numpy as np
from sklearn.linear_model import LinearRegression
from stocklab.portfolio.portfolio import Portfolio
from stocklab.strategy.abs import Strategy
from stocklab.vars import *
from stocklab.strategy.order import Order, Orders


class BasicStrategy(Strategy):
    STOP_LOSS = -0.01
    TAKE_PROFIT = 0.01

    def __init__(self, *args, **kwargs):
        self.price_index = COLS.high
        self.score_index = COLS.score
        self.state = None
        if "portfolio" in kwargs:
            self.portfolio = kwargs["portfolio"]
            self.setup_data()
            assert isinstance(self.portfolio, Portfolio)
        else:
            raise "portfolio is a must"

    def setup_data(self):
        for symbol in self.portfolio.symbols:
            symbol.df["Buy"] = [random.randint(0, 1) for _ in range(len(symbol.df))]
            symbol.df["Score"] = [random.random() for _ in range(len(symbol.df))]

    def decision(self, *args, **kwargs):
        state = kwargs["state"]
        index = kwargs["index"]
        orders = Orders()
        self.state = state
        for hold in state.holds.HOLDS:
            price = hold.symbol.get_by_index(index, self.price_index)
            if price:
                if self.should_sell(hold, price):
                    order = Order(op=ORDERS.sell, symbol=hold.symbol,
                                  hold=hold, price=price, score=1.0)
                    orders.add_order(order)

        for symbol in self.portfolio.symbols - self.state.holds.symbols:
            if self.should_buy(symbol, index):
                price = symbol.get_by_index(index, self.price_index)
                score = symbol.get_by_index(index, self.score_index)
                if price:
                    order = Order(op=ORDERS.buy, symbol=symbol,
                                  price=price, score=score)
                    orders.add_order(order)
        return orders

    def should_buy(self, *args, **kwargs) -> bool:
        symbol = kwargs["symbol"]
        index = kwargs["index"]
        if symbol in self.state.holds.symbols:
            return False
        row = symbol.get_by_index(index, "Buy")
        if row == 1:
            return True
        return False

    def should_sell(self, *args, **kwargs) -> bool:
        hold = kwargs["hold"]
        price = kwargs["price"]
        # take profit
        if hold.profit_pct(price) >= self.TAKE_PROFIT:
            return True
        # stop loss
        if hold.profit_pct(price) <= self.STOP_LOSS:
            return True
        return False

    def sell_fees(self, cash) -> float:
        return cash

    def buy_fees(self, cash) -> float:
        return cash

    def score(self):
        df = self.state.trades.to_df
        if not df.empty:
            trade_count = len(df[df["order"] == ORDERS.buy])
            win_count = len(df[df["profit"] > 0.0])
            loss_count = len(df[df["profit"] < 0.0])

            print(f"#trades {trade_count}")
            print(f"socre {win_count / (loss_count + win_count)}")

