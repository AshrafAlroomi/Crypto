import time
from flask import render_template, redirect, url_for, request
#from strategies.patterns import PatternStrategy, PatternStrategyByhour
from strategies.period import PatternWithIndicators
from ui.app import socket_app, app
from flask_socketio import emit
from data.binance import read_binance_data, get_symbols
from stocklab.portfolio.portfolio import Portfolio
from stocklab.backtest.simulation import Simulation
from threading import Lock

thread = None
thread_lock = Lock()


PORTFOLIO = Portfolio()
SIMULATION = None
STRATEGY = None
STOP = False
DELAY = 1.0


# views
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
    dates = dates
    STRATEGY = PatternWithIndicators(portfolio=PORTFOLIO)
    SIMULATION = Simulation(balance, STRATEGY, (dates, "date"))

    return render_template("simulation.html")


# rest api
@app.route("/stop", methods=['GET'])
def stop():
    print("stop")
    global STOP
    STOP = True
    SIMULATION.strategy.score()
    return {}


@app.route("/resume", methods=['GET'])
def resume():
    print("resume")
    global STOP
    STOP = False
    return {}


@app.route("/delay/<t>")
def delay(t):
    new_delay = float(t)
    if new_delay >= 0.0:
        global DELAY
        DELAY = new_delay
    return {}


# socket api
@socket_app.on("next")
def next_trade():
    assert isinstance(SIMULATION, Simulation)
    time.sleep(DELAY)
    if SIMULATION.execute and not STOP:
        emit("result", SIMULATION.get_json)
    else:
        SIMULATION.strategy.score()
        pass
