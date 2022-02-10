import pandas as pd

from maker.sr import ParLines
from strategies.patterns import BasicStrategy
from maker.utils import Dir


class SRStrategy(BasicStrategy):
    PERIOD = 30
    STOP_LOSS = -0.04
    TAKE_PROFIT = 0.04


    @staticmethod
    def line_analysis(line:ParLines,x:float):
        s = line.support
        r = line.resistance



    def create_data(self, df: pd.DataFrame):
        df["Buy"] = 0
        df["Signal"] = 0
        df["Score"] = 1
        data = df["close"].values
        line = None
        idx = self.PERIOD
        llt = 0  # line live time

        for i in range(len(data) - self.PERIOD):
            line = ParLines(data[i:i+self.PERIOD])
            idx += 1
            support_pre = line.support.y(idx)
            resistance_pre = line.resistance.y(idx)
            support_diff = (support_pre - data[i]) / data[i]
            resistance_diff = (data[i] - resistance_pre) / data[i]

            """
                for i in range(len(data) - self.PERIOD, self.PERIOD):
                    if line is not None:
                        support_pre = line.support.y(idx)
                        resistance_pre = line.resistance.y(idx)
        
                        support_diff = (support_pre - data[i]) / data[i]
                        resistance_diff = (data[i] - resistance_pre) / data[i]
        
                        llt += 1
                        if support_diff > 0.01:
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
