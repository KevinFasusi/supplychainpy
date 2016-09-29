# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
from decimal import Decimal

import numpy as np
import pandas as pd
from pandas import DataFrame

from supplychainpy._helpers import _data_cleansing
from supplychainpy._helpers._decorators import keyword_sniffer
from supplychainpy._helpers._enum_formats import FileFormats
from supplychainpy._helpers._enum_formats import PeriodFormats
from supplychainpy._helpers._data_cleansing import check_extension
from supplychainpy.bi.recommendation_generator import run_sku_recommendation_state_machine
from supplychainpy.inventory import analyse_uncertain_demand
from supplychainpy.inventory import economic_order_quantity
from supplychainpy.inventory.abc_xyz import AbcXyz
import warnings

from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

UNKNOWN = 'UNKNOWN'


@keyword_sniffer
def analyse(z_value: Decimal = 1.28, currency: str = 'USD', reorder_cost: Decimal = 10, interval_length: int = 12,
            interval_type: str = 'month', **kwargs):
    analysed_orders = UncertainDemand
    analysed_orders_collection = []
    try:
        if kwargs is not None:
            if kwargs.get('file_path') == UNKNOWN:
                converted_data = list(np.array(kwargs['df']))
                for i in converted_data:
                    sku_id, orders, unit_cost, lead_time, retail_price, quantity_on_hand, backlog = \
                        _unpack_row(row=i, interval_length=interval_length)
                    total_orders = 0
                    if quantity_on_hand is None:
                        quantity_on_hand = 0.0
                    for order in orders['demand']:
                        total_orders += int(order)
                        analysed_orders = _analyse_orders(orders=orders, sku_id=sku_id, lead_time=lead_time,
                                                          unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                          z_value=z_value, retail_price=retail_price,
                                                          quantity_on_hand=quantity_on_hand, currency=currency,
                                                          total_orders=total_orders)
                    analysed_orders_collection.append(analysed_orders)
                abc = AbcXyz(analysed_orders_collection)
                analysis_df = _convert_to_pandas_df(analysed_orders_collection)
                return analysis_df
            elif kwargs['file_path'] is not UNKNOWN:
                analysed_orders_collection = []
                item_list = {}

                item_list = _clean_file(file_type=kwargs['file_type'], file_path=kwargs['file_path'],
                                        interval_length=interval_length)

                for sku in item_list:
                    orders = {}

                    sku_id, unit_cost, lead_time, retail_price, quantity_on_hand = sku.get("sku_id",
                                                                                           "UNKNOWN_SKU"), sku.get(
                        "unit_cost"), sku.get(
                        "lead_time"), sku.get("retail_price"), sku.get("quantity_on_hand")

                    orders['demand'] = sku.get("demand")
                    total_orders = 0
                    if quantity_on_hand == None:
                        quantity_on_hand = 0.0
                    for order in orders['demand']:
                        total_orders += int(order)

                        analysed_orders = _analyse_orders(orders=orders, sku_id=sku_id, lead_time=lead_time,
                                                          unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                          z_value=z_value, retail_price=retail_price,
                                                          quantity_on_hand=quantity_on_hand, currency=currency,
                                                          total_orders=total_orders)

                    analysed_orders_collection.append(analysed_orders)
                abc = AbcXyz(analysed_orders_collection)
                # analysis = [i.orders_summary() for i in analysed_orders_collection]
                return analysed_orders_collection
            elif kwargs['raw_data']:
                if kwargs['raw_data'] > 2:
                    d = analyse_uncertain_demand.UncertainDemand(orders=kwargs['raw_data'], sku=kwargs['sku_id'],
                                                                 lead_time=kwargs['lead_time'],
                                                                 unit_cost=kwargs['unit_cost'],
                                                                 reorder_cost=reorder_cost,
                                                                 z_value=z_value,
                                                                 retail_price=kwargs['raw_data'],
                                                                 quantity_on_hand=kwargs['quantity_on_hand'],
                                                                 currency=currency)
                else:
                    raise ValueError("Data set too small. Please use a minimum of 3 entries.")
                return d.orders_summary_simple()

    except KeyError as e:
        print(e)


def _clean_file(file_type: str, file_path: str, interval_length: int):
    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            with open(file_path, 'r') as raw_data:
                item_list = (_data_cleansing.clean_orders_data_row(raw_data, interval_length))
                return item_list
        elif file_type == FileFormats.csv.name:
            with open(file_path, 'r') as raw_data:
                item_list = _data_cleansing.clean_orders_data_row_csv(raw_data, length=interval_length)
                return item_list
    else:
        incorrect_file = "Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter."
        raise Exception(incorrect_file)


def _unpack_row(row: list, interval_length: int):
    orders = {}
    sku_id = row[0]
    orders['demand'] = list(row[1:interval_length + 1])
    unit_cost = row[interval_length + 1]
    lead_time = row[interval_length + 2]
    retail_price = row[interval_length + 3]
    quantity_on_hand = row[interval_length + 4]
    backlog = row[interval_length + 5]
    return sku_id, orders, unit_cost, lead_time, retail_price, quantity_on_hand, backlog


def _convert_to_pandas_df(analysis: list) -> DataFrame:
    d = [i.orders_summary() for i in analysis]
    analysis_dict = {
        'sku': [i.get('sku') for i in d],
        'unit_cost': [i.get('unit_cost') for i in d],
        'quantity_on_hand': [i.get('quantity_on_hand') for i in d],
        'excess_stock': [i.get('excess_stock') for i in d],
        'shortages': [i.get('shortages') for i in d],
        'demand_variability': [i.get('demand_variability') for i in d],
        'currency': [i.get('currency') for i in d],
        'safety_stock': [i.get('safety_stock') for i in d],
        'average_orders': [i.get('average_orders') for i in d],
        'economic_order_quantity': [i.get('economic_order_quantity') for i in d],
        'standard_deviation': [i.get('standard_deviation') for i in d],
        'ABC_XYZ_Classification': [i.get('ABC_XYZ_Classification') for i in d],
        'economic_order_variable_cost': [i.get('economic_order_variable_cost') for i in d],
        'reorder_quantity': [i.get('reorder_quantity') for i in d],
        'total_orders': [i.get('total_orders') for i in d],
        'reorder_level': [i.get('reorder_level') for i in d],
        'revenue': [i.get('revenue') for i in d]
    }
    analysis_df = pd.DataFrame(analysis_dict,
                               columns=['sku', 'unit_cost', 'quantity_on_hand', 'excess_stock', 'shortages',
                                        'demand_variability', 'currency', 'safety_stock', 'average_orders',
                                        'economic_order_quantity', 'standard_deviation',
                                        'ABC_XYZ_Classification',
                                        'economic_order_variable_cost', 'reorder_quantity', 'total_orders',
                                        'reorder_level', 'revenue'])
    return analysis_df


def _analyse_orders(orders: dict, sku_id: str, lead_time: Decimal, unit_cost: Decimal, reorder_cost: Decimal,
                    z_value: Decimal, retail_price: Decimal, quantity_on_hand: Decimal, currency: str,
                    total_orders: float):
    analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders,
                                                               sku=sku_id,
                                                               lead_time=lead_time,
                                                               unit_cost=unit_cost,
                                                               reorder_cost=Decimal(reorder_cost),
                                                               z_value=Decimal(z_value),
                                                               retail_price=retail_price,
                                                               quantity_on_hand=quantity_on_hand,
                                                               currency=currency)
    average_orders = analysed_orders.average_orders
    reorder_quantity = analysed_orders.fixed_order_quantity
    eoq = economic_order_quantity.EconomicOrderQuantity(total_orders=float(total_orders),
                                                        reorder_quantity=float(reorder_quantity),
                                                        holding_cost=float(0.25),
                                                        reorder_cost=float(reorder_cost),
                                                        average_orders=average_orders,
                                                        unit_cost=float(unit_cost))
    analysed_orders.economic_order_qty = eoq.economic_order_quantity
    analysed_orders.economic_order_variable_cost = eoq.minimum_variable_cost

    return analysed_orders


# TODO-feature specify length of orders, start position and period (day, week, month, ...)
# in the analysis function specify service-level expected for safety stock, a default is specified in the class
def analyse_orders(data_set: dict, sku_id: str, lead_time: Decimal, unit_cost: Decimal, reorder_cost: Decimal,
                   z_value: Decimal, retail_price: Decimal, quantity_on_hand: Decimal, currency: str = 'USD') -> dict:
    """Analyse orders data for one sku using a dictionary.

    Analyses orders data for a single sku using the values in the data_set dict.

    Args:
        data_set (dict):        The orders data for a specified period.
        sku_id (str):           The unique id of the sku.
        lead_time (Decimal):    The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        unit_cost (Decimal):    The unit cost of the sku to the organisation.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock.
        retail_price (Decimal): The retail or standard price of the sku.
        quantity_on_hand (Decimal): The quantity currently on hand as of analysis or retrieving data set.

    Returns:
        dict:       The summary of the analysis, containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}

    Raises:
        ValueError: Dataset too small. Please use a minimum of 3 entries.


    Examples:

        yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}

        summary = model_inventory.analyse_orders(yearly_demand,
                                         sku_id='RX983-90',
                                         lead_time=Decimal(3),
                                         unit_cost=Decimal(50.99),
                                         reorder_cost=Decimal(400),
                                         z_value=Decimal(1.28),
                                         retail_price=Decimal(600),
                                         quantity_on_hand=Decimal(390))
    """
    if len(data_set) > 2:
        warnings.warn('Analyse orders function has been deprecated. Please use the analyse function',
                      DeprecationWarning)
        d = analyse_uncertain_demand.UncertainDemand(orders=data_set, sku=sku_id, lead_time=lead_time,
                                                     unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                     z_value=z_value, retail_price=retail_price,
                                                     quantity_on_hand=quantity_on_hand, currency=currency)
    else:
        raise ValueError("Data set too small. Please use a minimum of 3 entries.")
    return d.orders_summary_simple()


def analyse_orders_from_file_col(file_path, sku_id: str, lead_time: Decimal, unit_cost: Decimal,
                                 reorder_cost: Decimal, z_value: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = PeriodFormats.months.name, currency='USD') -> dict:
    """Analyse orders from file arranged in a single column

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (file):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        sku_id (str):           The unique id of the sku.
        lead_time (Decimal):    The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        unit_cost (Decimal):    The unit cost of the sku to the organisation.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.
        retail_price (Decimal): The price at which the sku is retailed.


    Returns:
        dict:       The summary of the analysis, containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    Example:


    """
    orders = {}
    file_type_processed = ''
    warnings.warn('Analyse orders function has been deprecated. Please use the analyse function', DeprecationWarning)
    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            with open(file_path, 'r') as raw_data:
                orders = _data_cleansing.clean_orders_data_col_txt(raw_data)
            file_type_processed = 'txt'
        elif file_type == FileFormats.csv.name:
            with open(file_path) as raw_data:
                orders = _data_cleansing.clean_orders_data_col_csv(raw_data)
            file_type_processed = 'csv'
    else:
        raise Exception("Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.")

    d = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id, lead_time=lead_time,
                                                 unit_cost=unit_cost, reorder_cost=reorder_cost, z_value=z_value,
                                                 period=period, retail_price=retail_price, currency=currency)
    log.debug('Raw data columnar from {} analysed'.format(file_type_processed))

    return d.orders_summary()


def analyse_orders_from_file_row(file_path: str, z_value: Decimal, reorder_cost: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = "month", length: int = 12, currency: str = 'USD') -> list:
    """Analyse multiple SKUs from a file with data arranged by row.

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (file):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.

    Returns:
        list:       A list of summaries containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    [{'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}, {'ABC_XYZ_Classification': 'AX',
                    'reorder_quantity': '258', 'revenue': '2090910.44', 'average_order': '539',
                    'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR481-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}]
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.


    """
    warnings.warn('Analyse orders function has been deprecated. Please use the analyse function', DeprecationWarning)
    orders = {}
    analysed_orders_summary = []
    analysed_orders_collection = []

    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            with open(file_path, 'r') as raw_data:
                item_list = (_data_cleansing.clean_orders_data_row(raw_data, length=length))
        elif file_type == FileFormats.csv.name:
            with open(file_path, 'r') as raw_data:
                item_list = _data_cleansing.clean_orders_data_row_csv(raw_data, length=length)

    else:
        unspecified_file = "Unspecified file type, Please specify 'csv' or 'text' for file_type parameter."
        raise Exception(unspecified_file)
    # maybe use an iterable instead of unpacking for constructor
    try:
        for sku in item_list:
            sku_id = sku.get("sku_id")
            unit_cost = sku.get("unit_cost")
            lead_time = sku.get("lead_time")

            quantity_on_hand = sku.get("quantity_on_hand")

            if quantity_on_hand == None:
                quantity_on_hand = 0.0
            orders['demand'] = sku.get("demand")

            analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id,
                                                                       lead_time=lead_time,
                                                                       unit_cost=unit_cost,
                                                                       reorder_cost=reorder_cost, z_value=z_value,
                                                                       retail_price=retail_price,
                                                                       quantity_on_hand=quantity_on_hand,
                                                                       currency=currency)

            analysed_orders_collection.append(analysed_orders)
            analysed_orders_summary.append(analysed_orders.orders_summary())
            orders = {}
            del analysed_orders
    except KeyError:
        print("The csv file is incorrectly formatted")
    return analysed_orders_summary


# TODO Remove hard coded holding cost and make it a parameter
def analyse_orders_abcxyz_from_file(file_path: str, z_value: Decimal, reorder_cost: Decimal,
                                    file_type: str = FileFormats.text.name,
                                    period: str = "month", length: int = 12, currency: str = 'USD') -> list:
    """Analyse orders data from file and returns ABCXYZ analysis

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (str):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        length (int):           The number of periods in the data-ser referenced from the second column of the row
                                onwards.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):       Type of 'file csv' or 'text'
        period (str):          The period of time the data points are bucketed into.

    Returns:
        AbcXyz:     An AbcXyz class object is returned.
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    """
    warnings.warn('Analyse orders function has been deprecated. Please use the analyse function', DeprecationWarning)
    analysed_orders_collection = []
    item_list = {}
    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            item_list = (_data_cleansing.clean_orders_data_row(f, length))
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            item_list = _data_cleansing.clean_orders_data_row_csv(f, length=length)
    else:
        incorrect_file = "Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter."
        raise Exception(incorrect_file)

    for sku in item_list:
        orders = {}

        sku_id, unit_cost, lead_time, retail_price, quantity_on_hand = sku.get("sku_id", "UNKNOWN_SKU"), sku.get(
            "unit_cost"), sku.get(
            "lead_time"), sku.get("retail_price"), sku.get("quantity_on_hand")

        orders['demand'] = sku.get("demand")
        total_orders = 0
        if quantity_on_hand == None:
            quantity_on_hand = 0.0
        for order in orders['demand']:
            total_orders += int(order)

        analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders,
                                                                   sku=sku_id,
                                                                   lead_time=lead_time,
                                                                   unit_cost=unit_cost,
                                                                   reorder_cost=Decimal(reorder_cost),
                                                                   z_value=Decimal(z_value),
                                                                   retail_price=retail_price,
                                                                   quantity_on_hand=quantity_on_hand, currency=currency)

        average_orders = analysed_orders.average_orders

        reorder_quantity = analysed_orders.fixed_order_quantity

        eoq = economic_order_quantity.EconomicOrderQuantity(total_orders=float(total_orders),
                                                            reorder_quantity=float(reorder_quantity),
                                                            holding_cost=float(0.25),
                                                            reorder_cost=float(reorder_cost),
                                                            average_orders=average_orders,
                                                            unit_cost=float(unit_cost))

        analysed_orders.economic_order_qty = eoq.economic_order_quantity
        analysed_orders.economic_order_variable_cost = eoq.minimum_variable_cost

        analysed_orders_collection.append(analysed_orders)

    abc = AbcXyz(analysed_orders_collection)

    return analysed_orders_collection


def recommendations(analysed_orders: dict, forecast: dict):
    return run_sku_recommendation_state_machine(analysed_orders=analysed_orders, forecast=forecast)

# the np method allows a numpy array to be used. This requires the specification of a period and length the data is
# supposed to cover. This method also allows the use of lead time arrays for calculating average leadtimes. There
# also be an analyse_orders_from_file_np. using the analyse_orders_np method to process each row.

# def analyse_orders_np(unit_cost: Decimal, period: np.array, z_value: Decimal, orders: np.array,
#                      lead_time_np: np.array = [],
#                      lead_time: Decimal = 0.00, length: int = 12) -> dict:
#    d = analyse_uncertain_demand.UncertainDemandNp(orders_np=orders, length=length, period=period)
#    d.print_period()



# rewrite all of the to deal with database tables and rows instead of csv files.
