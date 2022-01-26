from stocklab.strategy.order import Orders, Order
from stocklab.vars import *
from strategies.patterns import PatternStrategyByhour
import pandas as pd
from talib import EMA
import talib


class PatternWithIndicators(PatternStrategyByhour):
    PATTERN_LIST = ["CDLLONGLEGGEDDOJI"]
    STOP_LOSS = -0.02
    TAKE_PROFIT = 0.012
    TIME_LIMIT = 60 * 4  # 3 hours

    def create_data(self, df):
        df["Buy"] = 0
        df["Signal"] = 0
        df["ema_1"] = EMA(df[COLS.close], timeperiod=32)
        df["ema_2"] = EMA(df[COLS.close], timeperiod=16)
        df["ema_3"] = EMA(df[COLS.close], timeperiod=8)

        for f in self.PATTERN_LIST:
            func = eval(f"talib.{f}")
            vals = func(df[COLS.open], df[COLS.high], df[COLS.low], df[COLS.high])
            df["Signal"] += vals
        df["Score"] = df["Signal"]
        df["Buy"] = df["Signal"]
        return df

    def should_buy(self, symbol, index) -> bool:
        if symbol in self.state.holds.symbols:
            return False

        buy_signal = symbol.get_by_index(index, "Buy")
        if buy_signal > 0.0:
            ema_1 = symbol.get_by_index(index, "ema_1")
            ema_2 = symbol.get_by_index(index, "ema_2")
            ema_3 = symbol.get_by_index(index, "ema_3")
            if ema_3 > ema_2:
                return True
        return False


class PatternSupporter(PatternStrategyByhour):

    def create_data(self, df):
        return df
