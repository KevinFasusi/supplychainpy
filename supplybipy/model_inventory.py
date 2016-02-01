from decimal import Decimal
from supplybipy import data_cleansing
from supplybipy.demand import analyse_uncertain_demand, economic_order_quantity
from supplybipy.demand import summarise_demand
from supplybipy.demand.abc_xyz import AbcXyz
from supplybipy.enum_formats import FileFormats


# TODO-feature specify length of orders, start position and period (day, week, month, ...)
# in the analysis function specify service-level expected for safety stock, a default is specified in the class

def analyse_orders(data_set: dict, sku_id: str, lead_time: Decimal, unit_cost: Decimal, reorder_cost: Decimal,
                   z_value: Decimal) -> dict:
    if len(data_set) > 2:
        d = analyse_uncertain_demand.UncertainDemand(orders=data_set, sku=sku_id, lead_time=lead_time,
                                                     unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                     z_value=z_value)
    else:
        raise ValueError("Dictionary too small. Please use a minimum of 3 entries.")
    return d.orders_summary()


def analyse_orders_from_file_col(file_path: str, sku_id: str, lead_time: Decimal, unit_cost: Decimal,
                                 reorder_cost: Decimal, z_value: Decimal, file_type: str = "text",
                                 period: str = "month", length: int = 12) -> dict:

    if check_extension(file_path=file_path, file_type=file_type) and file_type == FileFormats.text.name:
        f = open(file_path, 'r')
        orders = data_cleansing.clean_orders_data_col_txt(f)
    elif check_extension(file_path=file_path, file_type=file_type) and file_type == FileFormats.csv.name:
        f = open(file_path)
        orders = data_cleansing.clean_orders_data_col_csv(f)
    else:
        raise Exception("Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.")
    f.close()
    d = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id, lead_time=lead_time,
                                                 unit_cost=unit_cost, reorder_cost=reorder_cost, z_value=z_value)
    return d.orders_summary()


def analyse_orders_from_file_row(file_path: str, z_value: Decimal, reorder_cost: Decimal, file_type: str = "text",
                                 period: str = "month", length: int = 12) -> list:
    orders = {}
    analysed_orders_summary = []
    analysed_orders_collection = []
    if file_path.endswith(".txt") and file_type.lower() == "text":
        f = open(file_path, 'r')
        item_list = (data_cleansing.clean_orders_data_row(f))
    elif file_path.endswith(".csv") and file_type.lower() == "csv":
        f = open(file_path)
        item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
    else:
        raise Exception("Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.")
    # maybe use an iterable instead of unpacking for constructor
    for sku in item_list:
        sku_id = sku.get("sku id")
        unit_cost = sku.get("unit cost")
        lead_time = sku.get("lead time")
        orders['demand'] = sku.get("demand")
        analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id,
                                                                   lead_time=lead_time,
                                                                   unit_cost=unit_cost,
                                                                   reorder_cost=reorder_cost, z_value=z_value)
        analysed_orders_collection.append(analysed_orders)
        analysed_orders_summary.append(analysed_orders.orders_summary())
        orders = {}
        del analysed_orders
    return analysed_orders_summary


def analyse_orders_abcxyz_from_file(input_file_path: str, z_value: float, reorder_cost: float, file_type: str = "text",
                                    period: str = "month", length: int = 12) -> AbcXyz:
    try:
        analysed_orders_collection = []

        if input_file_path.endswith(".txt") and file_type == "text":
            f = open(input_file_path, 'r')
            item_list = (data_cleansing.clean_orders_data_row(f))
        elif input_file_path.endswith(".csv") and file_type == "csv":
            f = open(input_file_path)
            item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
        else:
            raise Exception("Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.")

        for sku in item_list:
            orders = {}

            sku_id = sku.get("sku id")
            unit_cost = sku.get("unit cost")
            lead_time = sku.get("lead time")
            orders['demand'] = sku.get("demand")

            analysed_orders = analyse_uncertain_demand.UncertainDemand(orders, sku_id, lead_time,
                                                                       unit_cost,
                                                                       Decimal(reorder_cost), Decimal(z_value))

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
            # probably best to serialise and deserialise the output for the analysed demand classs

        abc = AbcXyz(analysed_orders_collection)
        abc.percentage_revenue()
        abc.cumulative_percentage_revenue()
        abc.abc_classification()
        abc.xyz_classification()
        a = summarise_demand.AnalyseOrdersSummary(abc.orders)
        abc.abcxyz_summary = a.classification_summary()

        # create functions for analysis metrics, count all tyeps of each category. value of each category,
        # percentage value of each category
        # function in class to print out graph
        # for sku in abc.demand:
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
        # def AbcXyz_Analysis(analysed_orders_summary):
        #   for sku in analysed_orders_summary
        #      count += sku.get("")


def check_extension(file_path: str, file_type: str) -> bool:
    if file_path.endswith(".txt") and file_type.lower() == "text":
        flag = True
    elif file_path.endswith(".csv") and file_type.lower() == "csv":
        flag = True
    else:
        flag = False
    return flag
