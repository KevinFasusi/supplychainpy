from decimal import Decimal
from enum import Enum

from supplybipy import data_cleansing
from supplybipy.orders import analyse_orders, economic_order_quantity
from supplybipy.orders import analyse_orders_summary
from supplybipy.orders.abc_xyz import AbcXyz

Period = Enum('Period', 'years quarters months week')


# in the analysis function specify service-level expected for safety stock, a default is specified in the class

def model_orders(data_set: dict, sku_id: str, lead_time: float, unit_cost: float, reorder_cost: float,
                 z_value: float) -> dict:
    d = analyse_orders.OrdersUncertainDemand(data_set, sku_id, lead_time, unit_cost, reorder_cost, z_value)
    return d.orders_summary()


def analyse_orders_from_file_col(file_path: str, sku_id: str, lead_time: float, unit_cost: float, reorder_cost: float,
                                 z_value: float) -> dict:
    f = open(file_path, 'r')
    item_list = data_cleansing.clean_orders_data_col(f)
    f.close()
    d = analyse_orders.OrdersUncertainDemand(item_list, sku_id, lead_time, unit_cost, reorder_cost, z_value)
    return d.orders_summary()


# need more output
def analyse_orders_from_file_row(input_file_path: str, z_value: Decimal, reorder_cost: Decimal) -> list:
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
            #

            for sku in item_list:
                sku_id = sku.get("sku id")
                unit_cost = sku.get("unit cost")
                lead_time = sku.get("lead time")
                orders['orders'] = sku.get("orders")
                analysed_orders = analyse_orders.OrdersUncertainDemand(orders=orders, sku=sku_id, lead_time=lead_time,
                                                                       unit_cost=unit_cost,
                                                                       reorder_cost=reorder_cost, z_value=z_value)
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

def analyse_orders_abcxyz_from_file(input_file_path: str, z_value: float, reorder_cost: float) -> AbcXyz:
    # if input_file_path.endswith(".txt"):
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
            orders = {}

            sku_id = sku.get("sku id")
            unit_cost = sku.get("unit cost")
            lead_time = sku.get("lead time")
            orders['orders'] = sku.get("orders")

            analysed_orders = analyse_orders.OrdersUncertainDemand(orders, sku_id, lead_time,
                                                                   unit_cost,
                                                                   reorder_cost, z_value)

            average_orders = analysed_orders.get_average_orders

            reorder_quantity = analysed_orders.fixed_order_quantity
            eoq = economic_order_quantity.EconomicOrderQuantity(reorder_quantity, 0.25, reorder_cost,
                                                                average_orders, unit_cost)

            analysed_orders.economic_order_qty = eoq.economic_order_quantity
            analysed_orders.economic_order_variable_cost = eoq.minimum_variable_cost

            analysed_orders_collection.append(analysed_orders)

            del analysed_orders
            del eoq
            del sku
            # sort from top to bottom calculate the percentage of revenue
            # probably best to serialise and deserialise the output for the analysed orders classs

        abc = AbcXyz(analysed_orders_collection)
        abc.percentage_revenue()
        abc.cumulative_percentage_revenue()
        abc.abc_classification()
        abc.xyz_classification()
        a = analyse_orders_summary.AnalyseOrdersSummary(abc.orders)
        abc.abcxyz_summary = a.classification_summary()

        # create functions for analysis metrics, count all tyeps of each category. value of each category,
        # percentage value of each category
        # function in class to print out graph
        # for sku in abc.orders:
        #    print('{:.2f}'.format(sku.percentage_revenue))
        #    print('{:.2f}'.format(sku.cumulative_percentage))
        #    print('{}'.format(sku.abc_classification))
        #    print('{}'.format(sku.xyz_classification))
        #   print(sku.abcxyz_classification)
        # for order in analysed_orders_collection:
        #    print(order.eoq.minimum_variable_cost)
        return abc
    except IOError as e:
        print("invalid file path: ", e)
    except ValueError as e:
        print("invalid value: ", e)
        # else:
        # raise ValueError("file name must end with .txt")
    return ""

    # def AbcXyz_Analysis(analysed_orders_summary):
    #   for sku in analysed_orders_summary
    #      count += sku.get("")
