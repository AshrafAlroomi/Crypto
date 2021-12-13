from stocklab.portfolio.symbols import Symbols


class Hold:
    def __init__(self, symbol=None, quantity=0, price=0.0, index_current=None):
        self.symbol = symbol
        self.quantity = quantity
        self.unit_price = price
        self.cost = price * quantity
        self.index_current = index_current

    def profit_pct(self, price):
        return (self.quantity * price - self.cost)/self.cost


class Holds:
    def __init__(self, holds=None):
        if holds is None:
            holds = []
        self.HOLDS = holds

    def add(self, hold):
        self.HOLDS.append(hold)

    def drop(self, hold):
        for i in range(len(self.HOLDS)):
            if self.HOLDS[i] == hold:
                self.HOLDS.pop(i)
                break

    def get(self, symbol):
        for h in self.HOLDS:
            if h.symbol == symbol:
                return h
        raise f"no hold for {symbol}"

    def get_symbols_list(self):
        if self.HOLDS:
            return self.symbols
        return []

    @property
    def symbols(self):
        s = Symbols()
        for hold in self.HOLDS:
            s.add(hold.symbol)
        return s

    @property
    def get_current_prices(self):
        h = {}
        for hold in self.HOLDS:
            h[hold.symbol] = hold.cost
        return h

    @property
    def to_dict(self):
        hold_list = []
        for hold in self.HOLDS:
            hold_dict = {}
            hold_dict["symbol"] = hold.symbol.name
            hold_dict["cost"] = hold.cost
            hold_dict["quantity"] = hold.quantity
            hold_dict["price"] = hold.unit_price
            hold_list.append(hold_dict)
        return hold_list
