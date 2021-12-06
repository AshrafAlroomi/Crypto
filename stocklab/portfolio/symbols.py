class Symbol(object):
    def __init__(self, name, pct, df):
        self.name = name
        self.pct = pct
        self.df = df

    def get_by_index(self, index, col):
        row = self.df.loc[self.df[index.col_name] == index.current][col]
        if not row.empty:
            return row.iloc[-1]
        return False


class Symbols:
    def __init__(self, symbols=None):
        if symbols is None:
            symbols = []
        self.SYMBOLS = symbols

    def add(self, symbol):
        self.SYMBOLS.append(symbol)

    def get(self, name):
        for s in self.SYMBOLS:
            if s.name == name:
                return s
        raise f"no symbols {name}"

    def __sub__(self, other):
        return set(self.SYMBOLS) - set(other)

    def __iter__(self):
        return self.SYMBOLS.__iter__()
