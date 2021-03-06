import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from maker.sr import ParLines, LinesTester
from strategies.patterns import BasicStrategy
from maker.utils import Dir
from stocklab.vars import *

"""
creat lines for each period 
test line efficiancy 
accept line 
make trade 
"""


class SRStrategy(BasicStrategy):
    PERIOD = 20
    PRICE_BUY_INDEX = COLS.close
    PRICE_SELL_INDEX = COLS.close
    STOP_LOSS = -0.05
    TAKE_PROFIT = 0.1

    def create_data(self, df: pd.DataFrame):
        df["Signal"] = 0
        df["Score"] = 1
        data = df["close"].values
        buy = np.zeros(len(df))
        line = None
        n_points = 0
        end_idx = 0
        start_idx = 0
        i = 0

        while i < len(data) - self.PERIOD:
            if line is None:
                n_points = 0
                start_idx = i + 1
                end_idx = i + self.PERIOD
                line = ParLines(data[i:end_idx], list(range(i, end_idx)))
                if line.resistance.dir == Dir.down:
                    pass
                else:
                    line = None
            else:
                if n_points < 35:
                    if line.support.y(i) < data[i] < line.resistance.y(i):
                        n_points += 1
                    else:
                        line = None
                        i = start_idx
                else:
                    n_points += 1
                    pre = line.resistance.y(i)
                    if data[i] > pre + (pre * 0.005):
                        buy[i] = 1
                        # tester = LinesTester(line)
                        # plt.plot(i, data[i], "x")
                        # tester.test(data[end_idx:i + 30])
                        line = None
                    elif data[i] < line.support.y(i):
                        line = None
                        i = start_idx
            i += 1
        df["Buy"] = buy
        return df
