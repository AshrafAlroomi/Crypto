import random
from stocklab.strategy.basic import BasicStrategy


class RandomStrategy(BasicStrategy):
    STOP_LOSS = -0.01
    TAKE_PROFIT = 0.01
    MID_DAY = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_data(self, df):
        df["Buy"] = [random.randint(0, 1) for _ in range(len(df))]
        df["Score"] = [random.random() for _ in range(len(df))]
        return df
