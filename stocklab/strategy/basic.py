import random

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from stocklab.portfolio.portfolio import Portfolio
from stocklab.strategy.abs import Strategy
from stocklab.vars import *
from stocklab.strategy.order import Order, Orders


class BasicStrategy(Strategy):
    STOP_LOSS = -0.01
    TAKE_PROFIT = 0.01
    PRICE_BUY_INDEX = COLS.close
    PRICE_SELL_INDEX = COLS.high

    def __init__(self, *args, **kwargs):
        self.score_index = COLS.score
        self.state = None
        if "portfolio" in kwargs:
            self.portfolio = kwargs["portfolio"]
            self.data()
            assert isinstance(self.portfolio, Portfolio)
        else:
            raise "portfolio is a must"

    def data(self):
        for symbol in self.portfolio.symbols:
            symbol.df = self.create_data(symbol.df)

    def create_data(self, df) -> pd.DataFrame:
        df["Buy"] = [random.randint(0, 1) for _ in range(len(df))]
        df["Score"] = [random.random() for _ in range(len(df))]
        return df

    def decision(self, *args, **kwargs):
        state = kwargs["state"]
        index = kwargs["index"]
        orders = Orders()
        self.state = state
        for hold in state.holds:
            price = hold.symbol.get_by_index(index, self.PRICE_SELL_INDEX)
            if price:
                if self.should_sell(hold=hold, price=price, index=index):
                    order = Order(op=ORDERS.sell, symbol=hold.symbol,
                                  hold=hold, price=price, score=1.0)
                    orders.add_order(order)

        for symbol in self.portfolio.symbols - self.state.holds.symbols:
            if self.should_buy(symbol=symbol, index=index):
                price = symbol.get_by_index(index, self.PRICE_BUY_INDEX)
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
        return cash - (cash * 0.01)

    def buy_fees(self, cash) -> float:
        return cash

    def score(self):
        df = self.state.trades.to_df
        if not df.empty:
            trade_count = len(df[df["order"] == ORDERS.buy])
            wins = df[df["profit"] > 0.0]["profit"].values
            losses = df[df["profit"] < 0.0]["profit"].values
            win_count = len(wins)
            loss_count = len(losses)
            win_avg = np.mean(wins)
            loss_avg = np.mean(losses)
            profit_avg = np.mean(df["profit"].values)
            score = win_count / (loss_count + win_count)

            return {"trades": trade_count, "score": round(score, 2), "avg": round(profit_avg, 2),
                    "wins": win_count, "losses": loss_count, "win_avg": round(win_avg, 3),
                    "loss_avg": round(loss_avg, 3)}
