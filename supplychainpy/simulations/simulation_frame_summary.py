from decimal import Decimal

from supplychainpy.simulations.monte_carlo_summary import MonteCarloSummary
from supplychainpy.simulations.simulation_window import MonteCarloWindow


class MonteCarloFrameSummary:
    def __init__(self):
        pass

    @staticmethod
    def summarise_frame(sim_window: list, window_size: int, orders_collection={}):

        while sim_window.position < window_size:




            frame_summary = MonteCarloSummary
            frame_summary.closing_stock_average = [sim_window.demand]
            yield orders_collection