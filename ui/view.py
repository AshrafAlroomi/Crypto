import time
from flask import render_template, redirect, url_for, request
from ui.app import socket_app, app
from flask_socketio import emit
from data.binance import read_binance_data, get_symbols
from stocklab.portfolio import Portfolio
from stocklab.simulation import Simulation
from strategies.midday import MidDayMulti

PORTFOLIO = Portfolio()
SIMULATION = None
STRATEGY = None
STOP = False


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        balance = 0
        coins = []
        values = []
        for k, v in request.form.to_dict().items():
            if k == "balance":
                balance = v
            elif len(k.split("_")) > 1:
                coin = k.split("_")[0]
                value = float(v)
                if 0.0 < value <= 1.0:
                    coins.append(coin)
                    values.append(str(value))
            else:
                pass
        if coins and balance and values:
            return redirect(url_for("start", coins=",".join(coins), values=",".join(values), balance=balance))

    symbols = get_symbols()
    return render_template("home.html", symbols=symbols)


@app.route("/start/<balance>/<coins>/<values>")
def start(balance, coins, values):
    global SIMULATION
    global STRATEGY
    if coins and balance and values:
        coins = coins.split(",")
        values = values.split(",")
        balance = int(balance)
    else:
        raise ValueError

    dates = []
    for i in range(len(coins)):
        df = read_binance_data(coins[i])
        new_dates = df["date"].values
        if len(dates) < len(new_dates):
            dates = new_dates
        PORTFOLIO.add_symbol(coins[i], float(values[i]), df)
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
