from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):

    @abstractmethod
    def setup_data(self) -> pd.DataFrame: pass

    @abstractmethod
    def decision(self, *args, **kwargs) -> tuple: pass

    @abstractmethod
    def should_buy(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def should_sell(self, *args, **kwargs) -> bool: pass

    @abstractmethod
    def fees(self) -> float: pass
