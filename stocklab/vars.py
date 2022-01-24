from dataclasses import dataclass


@dataclass
class ORDERS:
    buy = "Buy"
    sell = "Sell"
    hold = "Hold"


@dataclass
class COLS:
    index = "date"
    date = "date"
    close = "close"
    high = "high"
    low = "low"
    open = "open"
    score = "Score"
