from stocklab.backtest.holds import Holds, Hold
from stocklab.backtest.trades import Trades, Trade
from stocklab.strategy.order import Order
from stocklab.strategy.abs import Strategy
from stocklab.vars import ORDERS
from dataclasses import dataclass


@dataclass
class State:
    strategy: Strategy
    balance: int
    holds = Holds()
    trades = Trades()

    def sell(self, order: Order, index):
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
                hold = Hold(symbol=order.symbol, quantity=quantity, unit_price=order.price, index_current=index.current)
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
