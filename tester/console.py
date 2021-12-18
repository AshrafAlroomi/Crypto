import time
from tester.setup import *


def run(stdscr):
    stdscr.clear()
    stdscr.nodelay(1)
    key = ''
    time_sleep = 0
    pause = False
    while key != 'q':
        c = stdscr.getch()
        if c != -1:
            key = chr(c)
            if key == 's':
                pause = True
                score = strategy.score()
                stdscr.addstr(4, 65, str(score))
            elif key == 'r':
                pause = False
            elif key == 't':
                time_sleep += 0.01
            elif key == 'y':
                time_sleep -= 0.01
                time_sleep = abs(time_sleep)

        time.sleep(time_sleep)
        if not pause:
            if not sim.execute:
                break
            stdscr.clear()
            report = sim.get_json
            trades = report.get('trades')
            holds = report.get('holds')
            for i, hold in enumerate(holds):
                stdscr.addstr(i % 10, 0, f"hold: {hold.get('symbol')} cost:{hold.get('cost')}")

            for i, trade in enumerate(trades):
                stdscr.addstr(i % 10, 30, f"order: {trade.get('order')} {trade.get('name')}")

            stdscr.addstr(0, 150, f"time: {report.get('period')}")
            stdscr.addstr(1, 150, f"balance: {report.get('balance')}")
            stdscr.addstr(2, 150, f"assets: {report.get('assets')}")
            stdscr.addstr(3, 150, f"profit: {report.get('profit')}")
