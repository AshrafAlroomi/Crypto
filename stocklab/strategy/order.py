class Order:
    def __init__(self, op, symbol=None, hold=None, price=0, score=0):
        self.op = op
        self.hold = hold
        self.symbol = symbol
        self.price = price
        self.score = score

    def get_quantity(self, balance):
        return (balance * self.symbol.pct) // self.price


class Orders:
    def __init__(self, orders=None):
        if orders is None:
            orders = []
        self.ORDERS = orders

    def add_order(self, order):
        # add new order
        # based on score value
        if len(self.ORDERS) == 0:
            self.ORDERS.append(order)
        else:
            idx = len(self.ORDERS) - 1
            for i in range(len(self.ORDERS)):
                if self.ORDERS[i].score <= order.score:
                    idx = i
                    break
            self.ORDERS.insert(idx + 1, order)

    def __iter__(self):
        return self.ORDERS.__iter__()
