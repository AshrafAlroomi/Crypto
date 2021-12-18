from tester.setup import *


def run():
    while True:
        if sim.execute:
            print(sim.get_json.get("profit"))
            print(sim.get_json.get("period"))
        else:
            break
    strategy.score()
