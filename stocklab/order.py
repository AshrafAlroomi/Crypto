from stocklab.config import *


class Order:
    def __init__(self, op, symbol=None, hold=None, price=0):
        self.op = op
        if op == ORDERS.sell:
            self.hold = hold
        elif op == ORDERS.buy:
            self.symbol = symbol
        else:
            raise f"op {op} incorrect"
        self.price = price
