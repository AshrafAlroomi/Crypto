from munch import DefaultMunch

ORDERS = {
    "buy": "Buy",
    "sell": "Sell",
    "hold": "hold"
}
ORDERS = DefaultMunch.fromDict(ORDERS)
