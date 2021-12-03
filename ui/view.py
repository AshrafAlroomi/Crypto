import pandas as pd
from flask import render_template
from app import socket_app, app
from flask_socketio import send, emit

from data import read_binance_data
from stocklab.portfolio import Portfolio
from stocklab.simulation import Simulation
from strategies.midday import MidDayMulti

PORTFOLIO = Portfolio()
SIMULATIOM = None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/start')
def start(coins, balance):
    dates = []
    for coin in coins:
        df = read_binance_data(coin)
        new_dates = df["date"].values
        if len(dates) < new_dates:
            dates = new_dates
        PORTFOLIO.add_symbol(coin["symbol"], coin["pct"], df)

    strategy = MidDayMulti(portfolio=PORTFOLIO, dates=dates)
    SIMULATIOM = Simulation(balance, strategy)

    return render_template("index.html")


@socket_app.on("start_simulation")
def start_simulation():
    if isinstance(SIMULATIOM, Simulation):
        SIMULATIOM.by_date()


@socket_app.on("test")
def test():
    print("-" * 10)
    print("socket api is working")
    print("-" * 10)


@socket_app.on("trades")
def get_trades():
    for i in range(5):
        print('xxx')
        # send({"data": "d"}, json=True)
        emit("get_trades", {"d": "d"})


@socket_app.on("speed")
def set_speed():
    pass


@socket_app.on("symbols")
def symbols():
    pass


@socket_app.on("holds")
def holds():
    pass


@socket_app.on("profit")
def profit():
    pass
