import time

from flask import render_template, redirect, url_for, request
from ui.app import socket_app, app
from flask_socketio import emit
from data_reader.data import read_binance_data
from stocklab.portfolio import Portfolio
from stocklab.simulation import Simulation
from strategies.midday import MidDayMulti
from ui.forms import StartForm

PORTFOLIO = Portfolio()
SIMULATION = None
STRATEGY = None
STOP = False


@app.route('/', methods=["GET", "POST"])
def index():
    form = StartForm()
    if request.method == 'POST':
        form = StartForm(request.form)
        if form.validate():
            coins = form.coins.data
            balance = form.balance.data
            if coins and balance:
                coins = ",".join(coins)
                return redirect(url_for("start", coins=coins, balance=balance))
    return render_template("home.html", form=form)


@app.route("/start/<balance>/<coins>")
def start(balance, coins):
    global SIMULATION
    global STRATEGY
    if coins and balance:
        coins = coins.split(",")
        balance = int(balance)
    else:
        raise ValueError

    dates = []
    for coin in coins:
        df = read_binance_data(coin)
        new_dates = df["date"].values
        if len(dates) < len(new_dates):
            dates = new_dates
        PORTFOLIO.add_symbol(coin, 0.25, df)
    dates = dates[:50]
    STRATEGY = MidDayMulti(portfolio=PORTFOLIO)
    SIMULATION = Simulation(balance, STRATEGY, dates)

    return render_template("simulation.html")


@socket_app.on("next")
def next_trade():
    assert isinstance(SIMULATION, Simulation)
    time.sleep(1)
    if SIMULATION.execute and not STOP:
        emit("result", SIMULATION.get_json)
    else:
        emit("report", STRATEGY.score())


@socket_app.on("stop")
def stop_trading():
    print("stop")
    global STOP
    STOP = True


@socket_app.on("resume")
def resume_trading():
    print("resume")
    global STOP
    STOP = False
    next_trade()


@socket_app.on("test")
def test():
    print("socket api is working")
