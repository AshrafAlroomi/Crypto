from stocklab.strategy.order import Orders, Order
from stocklab.vars import *
from strategies.tests import BasicStrategy
import pandas as pd
import talib

BASIC = """CDL3LINESTRIKE
CDL3BLACKCROWS
CDL3INSIDE
CDL3WHITESOLDIERS
CDL3STARSINSOUTH"""
BASIC_LIST = [x.split(' ')[0] for x in BASIC.split('\n')]

"""

## func(open, high, low, close)

## tlib score signal system : 

+200 bullish pattern with confirmation
+100 bullish pattern (most cases)
0 none
-100 bearish pattern
-200 bearish pattern with confirmation

"""


class PatternStrategy(BasicStrategy):
    STOP_LOSS = -0.03
    TAKE_PROFIT = 0.02

    def setup_data(self):

        for symbol in self.portfolio.symbols:
            symbol.df["Buy"] = 0
            symbol.df["Signal"] = 0
            for f in BASIC_LIST:
                func = eval(f"talib.{f}")
                vals = func(symbol.df[COLS.open], symbol.df[COLS.high], symbol.df[COLS.low], symbol.df[COLS.high])
                symbol.df["Signal"] += vals
            symbol.df["Score"] = symbol.df["Signal"]
            symbol.df["Buy"] = symbol.df["Signal"].apply(lambda x: self.buy_signal(x))

    @staticmethod
    def buy_signal(x):
        if x > 0:
            return 1
        return 0


class PatternStrategyByhour(BasicStrategy):
    PATTERN_LIST = ['CDL3LINESTRIKE',
                    'CDLINVERTEDHAMMER',
                    'CDLXSIDEGAP3METHODS',
                    'CDLGAPSIDESIDEWHITE']
    STOP_LOSS = -0.03
    TAKE_PROFIT = 0.012
    TIME_LIMIT = 60 * 8  # 3 hours
    REASON_TAKE_PROFIT = "TAKE_PROFIT"
    REASON_STOP_PROFIT = "STOP_LOSS"
    REASON_TIME_LIMIT = "TIME_LIMIT"

    def setup_data(self):
        for symbol in self.portfolio.symbols:
            symbol.df["Buy"] = 0
            symbol.df["Signal"] = 0
            for f in self.PATTERN_LIST:
                func = eval(f"talib.{f}")
                vals = func(symbol.df[COLS.open], symbol.df[COLS.high], symbol.df[COLS.low], symbol.df[COLS.high])
                symbol.df["Signal"] += vals
            symbol.df["Score"] = symbol.df["Signal"]
            symbol.df["Buy"] = symbol.df["Signal"].apply(lambda x: self.buy_signal(x))

    def decision(self, state, index):
        orders = Orders()
        self.state = state
        for hold in state.holds.HOLDS:
            price = hold.symbol.get_by_index(index, self.PRICE_SELL_INDEX)
            if price:
                should_sell, reason = self.should_sell(hold, price, index)
                if should_sell:
                    if reason == self.REASON_TAKE_PROFIT:
                        price = hold.symbol.get_by_index(index, COLS.high)

                    elif reason == self.REASON_TIME_LIMIT:
                        price = hold.symbol.get_by_index(index, COLS.close)

                    elif reason == self.REASON_STOP_PROFIT:
                        price = hold.symbol.get_by_index(index, COLS.close)
                    else:

                        raise ValueError

                    order = Order(op=ORDERS.sell, symbol=hold.symbol,
                                  hold=hold, price=price, score=1.0)
                    orders.add_order(order)

        for symbol in self.portfolio.symbols.SYMBOLS:
            if symbol not in self.state.holds.symbols.SYMBOLS:
                if self.should_buy(symbol=symbol, index=index):
                    price = symbol.get_by_index(index, self.PRICE_BUY_INDEX)
                    score = symbol.get_by_index(index, self.score_index)
                    if price:
                        order = Order(op=ORDERS.buy, symbol=symbol,
                                      price=price, score=score)
                        orders.add_order(order)
        return orders

    def should_buy(self, symbol, index) -> bool:
        if symbol in self.state.holds.symbols:
            return False
        buy_signal = symbol.get_by_index(index, "Buy")
        if buy_signal == 1:
            return True
        return False

    def should_sell(self, hold, price, index):
        period = index.current - hold.index_current
        diff = period.astype('timedelta64[m]')
        lowest_price = hold.symbol.get_by_index(index, COLS.low)
        if diff > self.TIME_LIMIT:
            return True, self.REASON_TIME_LIMIT

        if hold.profit_pct(price) >= self.TAKE_PROFIT:
            return True, self.REASON_TAKE_PROFIT

        if hold.profit_pct(lowest_price) <= self.STOP_LOSS:
            return True, self.REASON_STOP_PROFIT

        return False, None

    def sell_fees(self, cash) -> float:
        return cash - (cash * 0.01)

    @staticmethod
    def buy_signal(x):
        if x > 0:
            return 1
        return 0
