from stocklab.strategy.order import Orders, Order
from stocklab.vars import *
from strategies.patterns import PatternStrategyByhour
from strategies.tests import BasicStrategy
import pandas as pd
from talib import EMA
import talib


class PatternWithIndicators(PatternStrategyByhour):
    PATTERN_LIST = ["CDLLONGLEGGEDDOJI"]

    def setup_data(self):

        for symbol in self.portfolio.symbols:
            symbol.df["Buy"] = 0
            symbol.df["Signal"] = 0
            symbol.df["ema_1"] = EMA(symbol.df[COLS.close], timeperiod=32)
            symbol.df["ema_2"] = EMA(symbol.df[COLS.close], timeperiod=16)
            symbol.df["ema_3"] = EMA(symbol.df[COLS.close], timeperiod=8)

            for f in self.PATTERN_LIST:
                func = eval(f"talib.{f}")
                vals = func(symbol.df[COLS.open], symbol.df[COLS.high], symbol.df[COLS.low], symbol.df[COLS.high])
                symbol.df["Signal"] += vals
            symbol.df["Score"] = symbol.df["Signal"]
            symbol.df["Buy"] = symbol.df["Signal"]

    def should_buy(self, symbol, index) -> bool:
        if symbol in self.state.holds.symbols:
            return False

        buy_signal = symbol.get_by_index(index, "Buy")
        if buy_signal > 0.0:
            ema_1 = symbol.get_by_index(index, "ema_1")
            ema_2 = symbol.get_by_index(index, "ema_2")
            ema_3 = symbol.get_by_index(index, "ema_3")
            if ema_3 < ema_2:
                return True
        return False
