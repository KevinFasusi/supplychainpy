from decimal import Decimal

from supplychainpy import model_inventory


def run_monte_carlo(file_path: str, opening_stock: int, z_value: Decimal, reorder_cost: Decimal, file_type: str,
                runs: int, ) -> dict:
    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path,
                                                                      z_value=z_value,
                                                                      reorder_cost=reorder_cost,
                                                                      file_type=file_type)
    list_random_orders = []
    for i in range(0, runs):
        simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
        list_random_orders.append(simulation.normal_random_distribution)
        del simulation
