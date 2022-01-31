import pandas as pd
from maker.sr import StraightLines, ParLines, PeaksLines
from maker.sr import LinesTester


def get_data():
    path = '../data/dfs/Binance_NEOUSDT_1h.csv'
    df = pd.read_csv(path, skiprows=1).iloc[::-1]
    return df["close"].values


def test_all(s_idx, period):
    data = get_data()
    for method in [StraightLines, ParLines, PeaksLines]:
        lines = method(data[s_idx:s_idx + period])
        tester = LinesTester(lines)
        tester.test(data[s_idx + period:s_idx + period * 2])


def test_one(method, s_idx, period):
    data = get_data()
    lines = method(data[s_idx:s_idx + period])
    tester = LinesTester(lines)
    tester.test(data[s_idx + period:s_idx + period * 2])


if __name__ == '__main__':
    # test_all(3550, 40)
    test_one(PeaksLines, 3550, 40)
