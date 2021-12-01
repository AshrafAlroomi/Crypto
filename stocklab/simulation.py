import matplotlib.pyplot as plt
import numpy as np
import uuid
from abc import ABC, abstractmethod

"""
only for long positions 
one tik

"""


class Strategy(ABC):
    def __init__(self):
        self.logs = {}

    @abstractmethod
    def take_profit(self):
        pass

    @abstractmethod
    def stop_loss(self):
        pass

    @staticmethod
    def trade_id():
        return uuid.uuid4().hex[:6]


class Simulation:
    def __init__(self, balance, prices, orders, symbols):
        self.balance = balance
        self.prices = prices
        self.orders = orders
        self.symbol = symbols
        self.positions = {}

    def init_hold(self):
        for s in self.symbol:
            self.positions[s]["amount"] = 0

    def update_holds(self, symbol, amount, op="add"):
        if op == "sub":
            self.positions[symbol] -= amount
        elif op == "add":
            self.positions[symbol] += amount
        else:
            raise Exception

    def buy(self, symbol, price):
        amount = self.positions[symbol]["amount"]
        self.balance += amount * price
        self.update_holds(symbol, amount, "add")

        self.log("buy", price, amount)

    def sell(self, symbol, price):
        amount = self.positions[symbol]["amount"]
        self.balance -= amount * price
        self.update_holds(symbol, amount, "sub")

        self.log("sell", price, amount)

    def log(self, op, price, amount):
        print_arg = f"{op}, {op} at= {price} | currant balance= {self.balance} | amount= {amount}"
        self.print_template(print_arg)

    @staticmethod
    def print_template(print_arg):
        print("-" * 10)
        print(print_arg)
        print("-" * 10)













    """
    def run_sim(self, testPrices, pre, balance):
        # print(testPrices[0])
        # print('xxxxxxxxxxxx')
        opsell = 0
        opbuy = 0
        profit = []
        b = balance
        equiti = 0
        stil_bal = 0
        days = 0
        uselessdays = 0
        dayslist = []
        profit_per = []
        d = 0
        for price, op in zip(testPrices, pre):
            days += 1
            if op == 'long' and equiti == 0:
                print('-' * 50)
                d = days
                opbuy += 1
                equiti = b // price
                stil_bal = b - (equiti * price)
                # print(stil_bal)
                bal = b

                print(opbuy, ' at day: ', days, ' buy    at : ', price, ' currant balance : ', bal, ' amount = ',
                      equiti)


            elif op == 'short' and equiti != 0:

                opsell += 1
                b = equiti * price + stil_bal

                dayslist.append(days - d)
                stil_bal = 0
                equiti = 0

                fprofit = b - bal
                fprofitper = fprofit / bal
                profit_per.append(fprofitper)
                profit.append(fprofit)

                print(opsell, ' at day: ', days, ' closed at : ', price, ' currant balance : ', b, ' profit = ',
                      fprofit, ' per% = ', fprofitper)
                print('period = ', days - d)
                print('\n')
            elif equiti == 0 and op == 'short':
                uselessdays += 1

        fig = plt.figure(figsize=(20, 10))
        plt.plot(profit, 'g*')
        plt.plot(profit)

        plt.axhline(0, color='red')
        plt.show()
        print(stil_bal)

        self.printSummary(testPrices, opsell, opbuy, b, balance, profit, uselessdays, np.array(dayslist),
                          np.array(profit_per))

    def printSummary(testPrices, opsell, opbuy, b, balance, profit, uselessdays, dayslist, profit_per):
        profit = np.array(profit)
        print('\n')

        print('days = ', len(testPrices))
        print('\n')
        print('avg hold days = ', np.average(dayslist))
        print('\n')
        print('useless days : ', uselessdays)
        print('\n')

        print('num of pos = ', 'close ', opsell, ' open ', opbuy)
        print('\n')

        print('final balance = ', b)
        print('\n')

        print('profit = ', np.round((b / balance) * 100, 0), ' % ')
        print('\n')

        print('avg profit per day = ', b / len(testPrices))
        print('\n')
        print('avg profit per trade = ', b / opsell, '  ', np.average(profit_per), ' %')
        print('\n')
        print('Max min = ', max(profit), '  ', min(profit))
        print('\n')
        print('sum of loss = ', sum(profit[profit < 0]), ' count = ', len(profit[profit < 0]))
        print('\n')


class multiSim():
    def run_sim(testPrices, pres, stocks, balance, daypreiod=0):
        if daypreiod == 0:
            daypreiod = len(testPrices[0])

        numstocks = len(stocks)
        opsell = 0
        opbuy = 0
        profit = []
        b = balance
        equiti = 0
        stil_bal = 0
        days = 0
        uselessdays = 0
        dayslist = []
        profit_per = []
        d = 0
        stockindex = 0
        for days in range(daypreiod):
            for i in range(numstocks):
                op = pres[i][days]
                price = testPrices[i][days]
                if op == 'long' and equiti == 0:
                    print('-' * 50)
                    d = days
                    opbuy += 1
                    equiti = b // price
                    stil_bal = b - (equiti * price)
                    # print(stil_bal)
                    bal = b
                    stockindex = i

                    print(stocks[stockindex], opbuy, ' at day: ', days, ' buy    at : ', price, ' currant balance : ',
                          bal, ' amount = ', equiti)

                elif op == 'short' and equiti != 0 and stockindex == i:

                    opsell += 1
                    b = equiti * price + stil_bal

                    dayslist.append(days - d)
                    stil_bal = 0
                    equiti = 0

                    fprofit = b - bal
                    fprofitper = fprofit / bal
                    profit_per.append(fprofitper)
                    profit.append(fprofit)

                    print(stocks[stockindex], opsell, ' at day: ', days, ' closed at : ', price, ' currant balance : ',
                          b, ' profit = ', fprofit, ' per% = ', fprofitper)
                    print('period = ', days - d)
                    print('\n')

                elif equiti == 0 and op == 'short':
                    uselessdays += 1
        fig = plt.figure(figsize=(20, 10))
        plt.plot(profit, 'g*')
        plt.plot(profit)

        plt.axhline(0, color='red')
        plt.show()
        print(stil_bal)

        multiSim.printSummary(daypreiod, opsell, opbuy, b, balance, profit, uselessdays, np.array(dayslist),
                              np.array(profit_per))

    def printSummary(daypreiod, opsell, opbuy, b, balance, profit, uselessdays, dayslist, profit_per):
        profit = np.array(profit)
        print('\n')

        print('days = ', daypreiod)
        print('\n')
        print('avg hold days = ', np.average(dayslist))
        print('\n')
        print('useless days : ', uselessdays)
        print('\n')

        print('num of pos = ', 'close ', opsell, ' open ', opbuy)
        print('\n')

        print('final balance = ', b)
        print('\n')

        print('profit = ', np.round((b / balance) * 100, 0), ' % ')
        print('\n')

        print('avg profit per day = ', b / daypreiod)
        print('\n')
        print('avg profit per trade = ', b / opsell, '  ', np.average(profit_per), ' %')
        print('\n')
        print('Max min = ', max(profit), '  ', min(profit))
        print('\n')
        print('sum of loss = ', sum(profit[profit < 0]), ' count = ', len(profit[profit < 0]))
        print('\n')
"""
