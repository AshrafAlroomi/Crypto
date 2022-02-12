import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from maker.sr import ParLines, LinesTester
from strategies.patterns import BasicStrategy
from maker.utils import Dir

"""
creat lines for each period 
test line efficiancy 
accept line 
make trade 
"""


class SRStrategy(BasicStrategy):
    PERIOD = 20
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
                        #tester = LinesTester(line)
                        #plt.plot(i, data[i], "x")
                        #tester.test(data[end_idx:i + 10])
                        line = None
                    elif data[i] < line.support.y(i):
                        line = None
                        i = start_idx
            i += 1
        df["Buy"] = buy
        """
        for i in range(len(data) - self.PERIOD):
            if line is not None:
                support_pre = line.support.y(idx)
                resistance_pre = line.resistance.y(idx)

                support_diff = (support_pre - data[i]) / data[i]
                resistance_diff = (data[i] - resistance_pre) / data[i]

                llt += 1
                if support_diff > 0.05:
                    df.loc[i, 'Buy'] = -1
                if resistance_diff > 0.01:
                    line = None
                    df.loc[i, 'Buy'] = 1
                if llt == 20:
                    line = None
                else:
                    idx += 1
            else:
                line = ParLines(data[i:i + self.PERIOD])
                idx = self.PERIOD
                llt = 0
        """
        return df

    def should_buy(self, symbol, index) -> bool:

        if symbol in self.state.holds.symbols:
            return False
        row = symbol.get_by_index(index, "Buy")
        if row == 1:
            return True
        return False

    def should_sell(self, hold, price, index) -> bool:

        # take profit
        row = hold.symbol.get_by_index(index, "Buy")
        if row == -1:
            return True
        if hold.profit_pct(price) >= self.TAKE_PROFIT:
            return True
        # stop loss
        if hold.profit_pct(price) <= self.STOP_LOSS:
            return True
        return False
