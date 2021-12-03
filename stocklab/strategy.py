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

    def score(self):
        score_df = pd.DataFrame(self.state.trades)
        print("-" * 10)
        print("\n")
        sell = score_df[score_df.order == "Sell"]
        wins = sell[sell.profit > 0.0]
        print(f"#trades : {len(score_df)}")
        print(f"score : {len(wins) / len(sell)}")
        print("\n")
        print("-" * 10)
