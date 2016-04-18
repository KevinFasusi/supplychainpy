from operator import attrgetter


class SKU:
    def __init__(self, analysed_orders: object):
        self.__analysed_orders = analysed_orders

    def top_sku(self, attribute: str, count: int, reverse:bool =True)->dict:

        try:
            for index, sku in enumerate(sorted(self.__analysed_orders, key=attrgetter(attribute), reverse=reverse)):
                if index > count:
                    break
                yield sku.orders_summary()
        except AttributeError as e:
            possible_attributes = "Incorrect attribute provided as key. Please use one of the following:\n" \
                    "demand_variability\neconomic_order_quantity\naverage_order\nsafety_stock" \
                    "\nstandard_deviation\nreorder_level\nreorder_quantity\nrevenue\n" \
                    "economic_order_quantity\neconomic_order_variable_cost\n" \
                    "ABC_XYZ_Classification'\nexcess_stock\nshortages"
            print(possible_attributes)

