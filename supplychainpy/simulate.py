from multiprocessing.pool import ThreadPool
from decimal import Decimal
from supplychainpy import model_inventory
from supplychainpy.simulations import monte_carlo
from supplychainpy.simulations.simulation_frame_summary import MonteCarloFrameSummary
from supplychainpy.simulations.monte_carlo_frame import BuildFrame
import pyximport

pyximport.install()
from supplychainpy.simulations.sim_summary import summarize_monte_carlo, frame


def run_monte_carlo_mt(file_path: str, z_value: Decimal, runs: int, reorder_cost: Decimal,
                       file_type: str, period_length: int = 12) -> list:
    pool = ThreadPool(processes=4, )
    async_results = pool.apply_async(run_monte_carlo,
                                     (file_path, z_value, runs, reorder_cost, file_type, period_length,))

    return_val = async_results.get()

    return return_val


def run(simulation_frame: list, period_length: int = 12):
    pool = ThreadPool(processes=4, )
    async_results = pool.apply_async(summarize_window, (simulation_frame, period_length,))

    return_val = async_results.get()

    return return_val


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
                    [{'sku_id': 'KR202-209', 'revenue': '470157', 'quantity_sold': '1175', 'backlog': '0', 'index': '1',
                    'po_quantity': '3809', 'po_received': '', 'delivery': '0', 'closing_stock': '1175',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '1446', 'demand': '271',
                    'po_raised': 'PO 31', 'period': '1'}]
                    [{'sku_id': 'KR202-209', 'revenue': '470157', 'quantity_sold': '1175', 'backlog': '440', 'index':
                     '1', 'po_quantity': '5425', 'po_received': '', 'delivery': '0', 'closing_stock': '0',
                      'shortage_cost': '52801', 'shortage_units': '440.0126', 'opening_stock': '1175', 'demand': '1615',
                      'po_raised': 'PO 41', 'period': '2'}]
                    [{'sku_id': 'KR202-209', 'revenue': '663808', 'quantity_sold': '1659', 'backlog': '440', 'index':
                     '1', 'po_quantity': '3325', 'po_received': 'PO 31', 'delivery': '3810', 'closing_stock': '2100',
                      'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '0', 'demand': '1710',
                      'po_raised': 'PO 51', 'period': '3'}]
                    [{'sku_id': 'KR202-209', 'revenue': '1973009', 'quantity_sold': '4932', 'backlog': '0', 'index':
                    '1', 'po_quantity': '52', 'po_received': 'PO 41', 'delivery': '5425', 'closing_stock': '4933',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '2100', 'demand': '2592',
                    'po_raised': 'PO 61', 'period': '4'}]
                    [{'sku_id': 'KR202-209', 'revenue': '3018681', 'quantity_sold': '7546', 'backlog': '0', 'index':
                    '1', 'po_quantity': '0', 'po_received': 'PO 51', 'delivery': '3326', 'closing_stock': '7547',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '4933', 'demand': '711',
                    'po_raised': '', 'period': '5'}]
                    [{'sku_id': 'KR202-209', 'revenue': '2013648', 'quantity_sold': '5034', 'backlog': '0', 'index':
                    '1', 'po_quantity': '0', 'po_received': 'PO 61', 'delivery': '53', 'closing_stock': '5034',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '7547', 'demand': '2565',
                    'po_raised': '', 'period': '6'}]
                    [{'sku_id': 'KR202-209', 'revenue': '1479703', 'quantity_sold': '3699', 'backlog': '0', 'index':
                    '1', 'po_quantity': '1285', 'po_received': '', 'delivery': '0', 'closing_stock': '3699',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '5034', 'demand': '1335',
                    'po_raised': 'PO 91', 'period': '7'}]
                    [{'sku_id': 'KR202-209', 'revenue': '795256', 'quantity_sold': '1988', 'backlog': '0', 'index': '
                    1', 'po_quantity': '2996', 'po_received': '', 'delivery': '0', 'closing_stock': '1988',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '3699', 'demand': '1711',
                    'po_raised': 'PO 101', 'period': '8'}]
                    [{'sku_id': 'KR202-209', 'revenue': '728538', 'quantity_sold': '1821', 'backlog': '0', 'index': '1',
                     'po_quantity': '3163', 'po_received': 'PO 91', 'delivery': '1286', 'closing_stock': '1821',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '1988', 'demand': '1453',
                    'po_raised': 'PO 111', 'period': '9'}]
                    [{'sku_id': 'KR202-209', 'revenue': '1394888', 'quantity_sold': '3487', 'backlog': '0', 'index':
                    '1', 'po_quantity': '1497', 'po_received': 'PO 101', 'delivery': '2997', 'closing_stock': '3487',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '1821', 'demand': '1331',
                    'po_raised': 'PO 121', 'period': '10'}]
                    [{'sku_id': 'KR202-209', 'revenue': '2166626', 'quantity_sold': '5416', 'backlog': '0', 'index':
                    '1', 'po_quantity': '0', 'po_received': 'PO 111', 'delivery': '3164', 'closing_stock': '5417',
                    'shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '3487', 'demand': '1234',
                    'po_raised': '', 'period': '11'}]
                    [{'sku_id': 'KR202-209', 'revenue': '2300320', 'quantity_sold': '5750', 'backlog': '0', 'index':
                    '1', 'po_quantity': '0', 'po_received': 'PO 121', 'delivery': '1498', 'closing_stock': '5751', '
                    shortage_cost': '0', 'shortage_units': '0.000000', 'opening_stock': '5417', 'demand': '1164',
                    'po_raised': '', 'period': '12'}]


    """

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path,
                                                                      z_value=z_value,
                                                                      reorder_cost=reorder_cost,
                                                                      file_type=file_type)
    Transaction_report = []
    # add shortage cost,
    for k in range(0, runs):
        simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
        random_demand = simulation.generate_normal_random_distribution(period_length=period_length)
        for sim_window in simulation.build_window(random_normal_demand=random_demand, period_length=period_length):
            sim_dict = {"index": "{}".format(sim_window.index), "period": "{}".format(sim_window.position),
                        "sku_id": sim_window.sku_id, "opening_stock": "{}".format(round(sim_window.opening_stock)),
                        "demand": "{}".format(round(sim_window.demand)),
                        "closing_stock": "{}".format(round(sim_window.closing_stock)),
                        "delivery": "{}".format(round(sim_window.purchase_order_receipt_qty)),
                        "backlog": "{:.0f}".format(sim_window.backlog),
                        "po_raised": "{}".format(sim_window.po_number_raised),
                        "po_received": "{}".format(sim_window.po_number_received),
                        "po_quantity": "{:.0f}".format(int(sim_window.purchase_order_raised_qty)),
                        "shortage_cost": "{:.0f}".format(Decimal(sim_window.shortage_cost)),
                        "revenue": "{:.0f}".format(sim_window.revenue),
                        "quantity_sold": "{:0.0f}".format(sim_window.sold),
                        "shortage_units": "{:0f}".format(sim_window.shortage_units)}
            # so = BuildFrame(s=sim_dict)
            Transaction_report.append([sim_dict])
    return Transaction_report


def summarize_window(simulation_frame: list, period_length: int = 12):
    """ Summarizes the simulation window and provides the stockout percentage for each sku.

    Provides a summary for the full period length. The summary .
    Args:
       simulation_frame (list):     A collection of simulation windows.
       period_length (int):         The number of periods define the simulation window e.g. 12 weeks, months etc.

    Returns:
       dict:    A dict containing the results for each sku.{'maximum_opening_stock': 13181.0,
                'standard_deviation_closing_stock': 4407.468727436796, 'standard_deviation_backlog': 485.2568835735928,
                'variance_backlog': 235474.24305555542, 'minimum_backlog': 0.0, 'maximum_closing_stock': 13181.0,
                'standard_deviation_shortage_cost': 348.8327422580442, 'variance_opening_stock': 20387450.520833332,
                'average_opening_stock': 6350.75, 'minimum_quantity_sold': 0.0,
                'standard_deviation_opening_stock': 4515.246451837744, 'stockout_percentage': 0.0833333358168602,
                'maximum_backlog': 1337.0, 'sku_id': 'KR202-240', 'standard_deviation_revenue': 4489.574661244527,
                'maximum_quantity_sold': 13181.0, 'total_quantity_sold': 76742.0,
                'variance_quantity_sold': 20156280.638888914, 'minimum_closing_stock': 0.0,
                'variance_closing_stock': 19425780.583333332, 'variance_shortage_units': 121684.28207126712,
                'index': '32', 'average_closing_stock': 6461.5, 'total_shortage_units': 1337.80962,
                'maximum_shortage_units': 1266.604, 'minimum_shortage_units': 0.0, 'average_backlog': 216.9166717529297,
                'minimum_opening_stock': 0.0}
    """

    summary = summarize_monte_carlo(simulation_frame, period_length)

    return summary


def summarise_frame(window_summary):
    """ Summarizes the simulation frame
    Generates a summary for every window in run.

{'average_opening_stock': 4905.75, 'stockout_percentage': 0.1666666716337204, 'variance_shortage_units': 165381.7343624191, 'maximum_backlog': 1870.0, 'variance_quantity_sold': 12906093.138888916, 'standard_deviation_revenue': 3592.505134149277, 'maximum_closing_stock': 11718.0, 'minimum_opening_stock': 0.0, 'total_quantity_sold': 61238.0, 'minimum_shortage_units': 0.0, 'maximum_quantity_sold': 11718.0, 'maximum_opening_stock': 11718.0, 'standard_deviation_shortage_cost': 406.67153129081845, 'maximum_shortage_units': 1407.326, 'variance_closing_stock': 13806908.555555582, 'variance_opening_stock': 14506841.520833334, 'total_shortage_units': 2383.1461, 'index': '32', 'average_backlog': 279.75, 'average_closing_stock': 5029.66650390625, 'standard_deviation_opening_stock': 3808.7847826876928, 'minimum_closing_stock': 0.0, 'minimum_backlog': 0.0, 'minimum_quantity_sold': 0.0, 'standard_deviation_backlog': 524.1211890711282, 'standard_deviation_closing_stock': 3715.7648681739242, 'variance_backlog': 274703.0208333333, 'sku_id': 'KR202-240'}

    """

    frame_summary = frame(window_summary)
    return frame_summary
