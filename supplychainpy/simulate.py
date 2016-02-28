from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.simulations import monte_carlo
from supplychainpy.simulations.simulation_frame_summary import MonteCarloFrameSummary


def run_monte_carlo(file_path: str, z_value: Decimal, runs: int, reorder_cost: Decimal,
                    file_type: str, period_length: int = 12) -> list:
    """Runs monte carlo simulation.
    Generates random distribution for demand over period specified and creates a simulation window for opening_stock,
    demand, closing_stock, delivery and backlog for each sku in the data set.
    Args:
        file_path (str):        The path to the file containing two columns of data, 1 period and 1 data-point per sku.
        reorder_cost (Decimal): The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        period_length (int):    The number of periods define the simulation window e.g. 12 weeks, months etc.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided
                                by number.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        runs (int):             The number of times to run the simulation.

    Returns:
        list:       A list containing the results for each sku
                    [{'sku_id': 'KR202-209', 'demand': '3106', 'opening_stock': '1446', 'delivery': '0', 'closing_stock'
                    : '-3400', 'period': '1', 'index': '1', 'backlog': '1700'}]

    """

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path,
                                                                      z_value=z_value,
                                                                      reorder_cost=reorder_cost,
                                                                      file_type=file_type)
    sim_collection = []
    for k in range(0, runs):
        simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
        random_demand = simulation.generate_normal_random_distribution(period_length=period_length)
        for sim_window in simulation.build_window(random_normal_demand=random_demand, period_length=period_length):
            sim_dict = {"index": "{:.0f}".format(sim_window.index), "period": "{:.0f}".format(sim_window.position),
                        "sku_id": sim_window.sku_id, "opening_stock": "{:.0f}".format(sim_window.opening_stock),
                        "demand": "{:.0f}".format(sim_window.demand),
                        "closing_stock": "{:.0f}".format(sim_window.closing_stock),
                        "delivery": "{:.0f}".format(sim_window.purchase_order_receipt_qty),
                        "backlog": "{:.0f}".format(sim_window.backlog)}
            # so = BuildFrame(s=sim_dict)
            sim_collection.append([sim_dict])
    return sim_collection


def summarize_window(simulation_frame: list, period_length: int = 12) -> dict:
    """ Summarizes the simulation window and provides the stockout percentage for each sku.

    The summarize window provides a summary for each sku. The summary consists of probability of stockout based
    on current inventory metrics calculated with 'model_inventory.analyse_orders_abcxyz_from_file'.
    Args:
       simulation_frame (list):     A collection of simulation windows.
       period_length (int):         The number of periods define the simulation window e.g. 12 weeks, months etc.

    Yield:
       dict:       A dict containing the results for each sku.
    """

    closing_stock = []
    summary = MonteCarloFrameSummary
    for x in range(1, len(simulation_frame)):
        for f in simulation_frame:
            if int(f[0]['index']) == x:
                closing_stock.append(int(f[0]['closing_stock']))
            if len(closing_stock) == period_length:
                cls = summary.closing_stockout_percentage(closing_stock=closing_stock, period_length=period_length)
                summarize = {'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'index': f[0]['index']}
                yield summarize
                closing_stock = []
