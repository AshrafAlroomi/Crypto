from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):

    @abstractmethod
    def data(self): pass

    @abstractmethod
    def create_data(self, df) -> pd.DataFrame: pass

    @abstractmethod
    def decision(self, *args, **kwargs): pass

    @abstractmethod
    def should_buy(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def should_sell(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def sell_fees(self, cash) -> float: pass

    @abstractmethod
    def buy_fees(self, cash) -> float: pass

    @abstractmethod
    def score(self): pass
