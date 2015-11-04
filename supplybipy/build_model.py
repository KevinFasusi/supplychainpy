from enum import Enum
from decimal import Decimal
from operator import itemgetter, attrgetter
from supplybipy import analyse_orders
from supplybipy.analyse_orders import OrdersUncertainDemand
from supplybipy.lib import data_cleansing
from supplybipy.lib.abc_xyz import AbcXyz

Period = Enum('Period', 'years quarters months week')


# in the analysis function specify service-level expected for safety stock, a default is specified in the class

def model_orders(data_set, sku_id, lead_time, unit_cost, reorder_cost, z_value):
    """Models orders data in list data_set"""
    d = analyse_orders.OrdersUncertainDemand(data_set, sku_id, lead_time, unit_cost, reorder_cost, z_value)
    return d.orders_summary()


def analyse_orders_from_file_col(file_path, sku_id, lead_time, unit_cost, reorder_cost, z_value):
    """Retrieve data for a single sku in file with format 'period|value in a single column'"""
    f = open(file_path, 'r')
    item_list = data_cleansing.clean_orders_data_col(f)
    f.close()
    d = analyse_orders.OrdersUncertainDemand(item_list, sku_id, lead_time, unit_cost, reorder_cost, z_value)
    return d.orders_summary()


# need more output
def analyse_orders_from_file_row(input_file_path, z_value, reorder_cost):
    """Retrieve data for multiple skus from a .txt file with the format 'sku|value|value..."""
    if input_file_path.endswith(".txt"):
        try:
            orders = {}
            analysed_orders_summary = []
            analysed_orders_collection = []
            sku_id = []
            unit_cost = []
            lead_time = []
            f = open(input_file_path, 'r')
            out_file = open('orders_analysis.txt', 'w')
            item_list = (data_cleansing.clean_orders_data_row(f))
            for sku in item_list:
                sku_id = sku.get("sku id")
                unit_cost = sku.get("unit cost")
                lead_time = sku.get("lead time")
                orders['orders'] = sku.get("orders")
                analysed_orders = analyse_orders.OrdersUncertainDemand(orders, sku_id, lead_time,
                                                                       unit_cost,
                                                                       reorder_cost, z_value)
                analysed_orders_collection.append(analysed_orders)
                analysed_orders_summary.append(analysed_orders.orders_summary())
                orders = {}
                sku_id = []
                unit_cost = []
                lead_time = []
                del analysed_orders
        except IOError as e:
            print("invalid file path: ", e)
        except ValueError as e:
            print("invalid value: ", e)
    else:
        raise ValueError("file name must end with .txt")

    return analysed_orders_summary


# need to extract unit cost and lead time from file so can order skus by value and then ABC XYZ analysis
def analyse_orders_abcxyz_from_file(input_file_path, z_value, reorder_cost):
    """Retrieve data for multiple skus from a .txt file with the format 'sku|value|value..."""

    if input_file_path.endswith(".txt"):
        try:
            orders = {}
            analysed_orders_summary = []
            analysed_orders_collection = []
            sku_id = []
            unit_cost = []
            lead_time = []
            f = open(input_file_path, 'r')

            item_list = (data_cleansing.clean_orders_data_row(f))

            for sku in item_list:
                sku_id = sku.get("sku id")
                unit_cost = sku.get("unit cost")
                lead_time = sku.get("lead time")
                orders['orders'] = sku.get("orders")
                analysed_orders = analyse_orders.OrdersUncertainDemand(orders, sku_id, lead_time,
                                                                       unit_cost,
                                                                       reorder_cost, z_value)
                average_orders = analysed_orders.get_average_orders
                reorder_quantity = analysed_orders.fixed_order_quantity
                analyse_orders.OrdersUncertainDemand.eoq = analyse_orders.economic_order_quantity.EconomicOrderQuantity(
                    reorder_quantity, 0.25, reorder_cost, average_orders)
                average_orders = 0
                reorder_quantity = 0

                analysed_orders_summary.append(analysed_orders.orders_summary())
                analysed_orders_collection.append(analysed_orders)
                orders = {}
                sku_id = []
                unit_cost = []
                lead_time = []
                del analysed_orders
                # sort from top to bottom calculate the percentage of revenue
                # probably best to serialise and deserialise the output for the analysed orders classs

            abc = AbcXyz(analysed_orders_collection)
            abc.percentage_revenue()
            abc.cumulative_percentage_revenue()
            abc.abc_classification()
            abc.xyz_classification()

            for sku in abc.orders:
                print('{:.2f}'.format(sku.percentage_revenue))
                print('{:.2f}'.format(sku.cumulative_percentage))
                print('{}'.format(sku.abc_classification))
                print('{}'.format(sku.xyz_classification))
                print(sku.abcxyz_classification)
            for order in analysed_orders_collection:
                print(order.eoq.minimum_variable)

        except IOError as e:
            print("invalid file path: ", e)
        except ValueError as e:
            print("invalid value: ", e)
    else:
        raise ValueError("file name must end with .txt")

    return analysed_orders_collection
