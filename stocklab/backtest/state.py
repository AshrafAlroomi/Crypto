from stocklab.backtest.holds import Holds, Hold
from stocklab.backtest.trades import Trades, Trade
from stocklab.vars import ORDERS


class State:
    def __init__(self, balance, strategy):
        self.strategy = strategy
        self.balance = balance
        self.holds = Holds()
        self.trades = Trades()

    def sell(self, order, index):
        if self.can_sell:
            # del hold
            self.holds.drop(order.hold)
            # create trade
            trade = Trade(index, ORDERS.sell)
            trade.new(self, order)
            self.trades.add(trade)
            return True
        return False

    def buy(self, order, index):
        if self.can_buy:
            # get how many unit can buy
            quantity = order.get_quantity(self.balance)
            if quantity > 0:
                # create hold
                hold = Hold(order.symbol, quantity, order.price)
                self.holds.add(hold)
                # add hold to order obj
                order.hold = hold
                # create trade
                trade = Trade(index, ORDERS.buy)
                trade.new(self, order)
                self.trades.add(trade)
                return True
        return False

    @property
    def get_assets(self):
        assets = self.balance
        for h in self.holds.HOLDS:
            assets += h.cost
        return assets

    @property
    def can_buy(self):
        return True

    @property
    def can_sell(self):
        return True
