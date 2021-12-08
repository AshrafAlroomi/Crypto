from munch import DefaultMunch

ORDERS = {
    "buy": "Buy",
    "sell": "Sell",
    "hold": "hold"
}
COLS = {
    "index": "date",
    "date": "date",
    "close": "close",
    "high": "high",
    "low": "low",
    "open": "open",
    "score": "Score",

}

ORDERS = DefaultMunch.fromDict(ORDERS)
COLS = DefaultMunch.fromDict(COLS)
