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
from supplychainpy.bi.recommendation_generator import run_sku_recommendation, run_profile_recommendation
from supplychainpy.inventory import analyse_uncertain_demand
from supplychainpy.inventory import economic_order_quantity
from supplychainpy.inventory.abc_xyz import AbcXyz
import warnings

from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

UNKNOWN = 'UNKNOWN'


@keyword_sniffer
def analyse(currency: str, z_value: Decimal = 1.28, reorder_cost: Decimal = 10, interval_length: int = 12,
            interval_type: str = 'month', **kwargs):
    """ Performs several types of common inventory analysis on the raw demand data. Including safety stock, reorder
    levels.

    Args:
        currency (Decimal):             Currency the raw data is stored in.
        z_value (Decimal):              Service level requirement
        reorder_cost (Decimal):         Cost to place a reorder based on the cost of operations over the period
        interval_length (Decimal):      The number of periods the demand data is grouped into e.g. 12 (months)
        interval_type (Decimal):        months, weeks,days, years, quarters.

    Keyword Args:
        **df(pd.DataFrame):             Pandas DataFrame containing the raw data in the correct format.
        **file_path (str) :             Path to csv or txt file containing formatted data.

    Returns:
        dict/pd.DataFrame:  Analysis of inventory profile.

    Examples:

        >>> from supplychainpy.model_inventory import analyse
        >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
        >>> from decimal import Decimal
        >>> analysed_data = analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
        ...                         z_value=Decimal(1.28),
        ...                         reorder_cost=Decimal(400),
        ...                         retail_price=Decimal(455),
        ...                         file_type='csv',
        ...                         currency='USD')
        >>> analysis = [demand.orders_summary() for demand in analysed_data]
        >>> # Example using pandas DataFrame.
        >>> import pandas as pd
        >>> raw_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
        >>> analyse_kv = dict(
        ...     df=raw_df,
        ...     start=1,
        ...     interval_length=12,
        ...     interval_type='months',
        ...     z_value=Decimal(1.28),
        ...     reorder_cost=Decimal(400),
        ...     retail_price=Decimal(455),
        ...     file_type='csv',
        ...     currency='USD'
        ... )
        >>> analysis_df = analyse(**analyse_kv)
    """

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
                                                      total_orders=total_orders, backlog=backlog)
                    analysed_orders_collection.append(analysed_orders)
                AbcXyz(analysed_orders_collection)
                analysis_df = _convert_to_pandas_df(analysed_orders_collection)
                return analysis_df
            elif kwargs['file_path'] is not UNKNOWN:
                analysed_orders_collection = []
                item_list = _clean_file(file_type=kwargs['file_type'], file_path=kwargs['file_path'],
                                        interval_length=interval_length)
                for sku in item_list:
                    orders = {}
                    sku_id, unit_cost, lead_time, retail_price, quantity_on_hand, backlog = sku.get("sku_id","UNKNOWN_SKU"), \
                                                                                   sku.get("unit_cost"), \
                                                                                   sku.get("lead_time"), \
                                                                                   sku.get("retail_price"), \
                                                                                   sku.get("quantity_on_hand"), \
                                                                                   sku.get("backlog")
                    orders['demand'] = sku.get("demand")
                    total_orders = 0
                    if quantity_on_hand is None:
                        quantity_on_hand = 0.0
                    for order in orders['demand']:
                        total_orders += int(order)
                    analysed_orders = _analyse_orders(orders=orders, sku_id=sku_id, lead_time=lead_time,
                                                      unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                      z_value=z_value, retail_price=retail_price,
                                                      quantity_on_hand=quantity_on_hand, currency=currency,
                                                      total_orders=total_orders, backlog=backlog)
                    analysed_orders_collection.append(analysed_orders)
                AbcXyz(analysed_orders_collection)
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


def _clean_file(file_type: str, file_path: str, interval_length: int) -> dict:
    """ Cleans-up csv and txt files and validates the format.

    Args:
        file_type (str):            'csv' or 'txt' file type.
        file_path (str) :           Absolute path to file.
        interval_length (int):      The number of periods included in raw data.

    Returns:
        dict:   Sanitised source data.

    """
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


def _unpack_row(row: list, interval_length: int) -> tuple:
    """ Retrieves data-points based on fixed hardcoded positions in source file.

    Args:
        row (list):                 Row of data from source file.
        interval_length (int):      The number of periods included in raw data.

    Returns:
        tuple:      Separate data points (orders, sku_id, unit_cost, lead_time, retail_price, quantity_on_hand, backlog)

    """
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
    """ Converts list of dicts to Pandas Dataframe with the correct orientation.

    Args:
        analysis (list):    Collection of analysed SKU data.

    Returns:
        DataFrame:     Converted DataFrame.

    """
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
                    total_orders: float, backlog: Decimal) -> UncertainDemand:
    """ Performs several types of common inventory analysis on the raw demand data. Including safety stock, reorder
    levels.

    Args:
        orders (dict):
        sku_id (str):
        lead_time (Decimal):
        unit_cost (Decimal):
        reorder_cost (Decimal):
        z_value (Decimal):
        retail_price (Decimal):
        quantity_on_hand (Decimal):
        currency (str):
        total_orders (float):

    Returns:
        UncertainDemand:    UncertainDemand objects.

    """
    analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders,
                                                               sku=sku_id,
                                                               lead_time=lead_time,
                                                               unit_cost=unit_cost,
                                                               reorder_cost=Decimal(reorder_cost),
                                                               z_value=Decimal(z_value),
                                                               retail_price=retail_price,
                                                               quantity_on_hand=quantity_on_hand,
                                                               currency=currency,
                                                               backlog=backlog)
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
        data_set (dict):            The orders data for a specified period.
        sku_id (str):               The unique id of the sku.
        lead_time (Decimal):        The average lead-time for the sku over the period represented by the data,
                                    in the same unit.
        unit_cost (Decimal):        The unit cost of the sku to the organisation.
        reorder_cost (Decimal):     The cost to place a reorder. This is usually the cost of the operation divided by
                                    number of purchase orders placed in the previous period.
        z_value (Decimal):          The service level required to calculate the safety stock.
        retail_price (Decimal):     The retail or standard price of the sku.
        quantity_on_hand (Decimal): The quantity currently on hand as of analysis or retrieving data set.
        currency (str):             Currency of source raw data.

    Returns:
        dict:       The summary of the analysis.

                    `{'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}`

    Raises:
        ValueError: Dataset too small. Please use a minimum of 3 entries.


    Examples:
        >>> from supplychainpy.model_inventory import analyse_orders
        >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
        >>> from decimal import Decimal
        >>> yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
        ...                 'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
        >>>
        >>> summary = analyse_orders(yearly_demand,
        ...                          sku_id='RX983-90',
        ...                          lead_time=Decimal(3),
        ...                          unit_cost=Decimal(50.99),
        ...                          reorder_cost=Decimal(400),
        ...                          z_value=Decimal(1.28),
        ...                          retail_price=Decimal(600),
        ...                          quantity_on_hand=Decimal(390))
    """
    if len(data_set) > 2:
        warnings.warn('The \'analyse_orders\' function has been deprecated. Please use the \'analyse\' function',
                      DeprecationWarning)
        d = analyse_uncertain_demand.UncertainDemand(orders=data_set, sku=sku_id, lead_time=lead_time,
                                                     unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                     z_value=z_value, retail_price=retail_price,
                                                     quantity_on_hand=quantity_on_hand, currency=currency)
    else:
        raise ValueError('Data set too small. Please use a minimum of 3 entries.')
    return d.orders_summary_simple()


def analyse_orders_from_file_col(file_path, sku_id: str, lead_time: Decimal, unit_cost: Decimal,
                                 reorder_cost: Decimal, z_value: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = PeriodFormats.months.name, currency='USD') -> dict:
    """ Analyse orders from file arranged in a single column.

    Analyses orders data for a single sku, using the values
    from a file arranged in columns.The data should be arranged in two columns, 1 for the period and the other for the
    corresponding data-point.

    Args:
        file_path (str):              The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        sku_id (str):                 The unique id of the sku.
        lead_time (Decimal):          The average lead-time for the sku over the period represented by the data, in the same unit.
        unit_cost (Decimal):          The unit cost of the sku to the organisation.
        reorder_cost (Decimal):       The cost to place a reorder. This is usually the cost of the operation divided by number of purchase orders placed in the previous period.
        z_value (Decimal):            The service level required to calculate the safety stock
        retail_price (Decimal):       The price at which the sku is retailed.
        file_type (str):              Type of 'file csv' or 'text'
        period (int):                 The period of time the data points are bucketed into.
        currency (str):               The currency of the source data.

    Returns:
        dict:   The summary of the analysis.

                `{'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                'standard_deviation': '28', 'safety_stock': '51'}`

    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    Examples:

    >>> from decimal import Decimal
    >>> from supplychainpy.model_inventory import analyse_orders_from_file_col
    >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
    >>> # text file
    >>> RX9304_43_analysis_txt = analyse_orders_from_file_col(file_path=ABS_FILE_PATH['PARTIAL_COL_TXT_SM'],
    ...                                                   sku_id='RX9304-43',
    ...                                                   lead_time=Decimal(2),
    ...                                                   unit_cost=Decimal(400),
    ...                                                   reorder_cost=Decimal(45),
    ...                                                   z_value=Decimal(1.28),
    ...                                                   file_type='text',
    ...                                                   retail_price=Decimal(30))
    >>> #csv file
    >>> RX9304_43_analysis_csv = analyse_orders_from_file_col(ABS_FILE_PATH['PARTIAL_COL_CSV_SM'], 'RX9304-43',
    ...                                                     reorder_cost=Decimal(45),
    ...                                                     unit_cost=Decimal(400),
    ...                                                     lead_time=Decimal(45),
    ...                                                     z_value=Decimal(1.28),
    ...                                                     file_type="csv",
    ...                                                     retail_price=Decimal(30))


    """
    orders = {}
    file_type_processed = ''
    # warnings.warn('Analyse orders function has been deprecated. Please use the analyse function', DeprecationWarning)
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
        raise Exception('Unspecified file type, Please specify \'csv\' or \'text\' for file_type parameter.')

    d = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id, lead_time=lead_time,
                                                 unit_cost=unit_cost, reorder_cost=reorder_cost, z_value=z_value,
                                                 period=period, retail_price=retail_price, currency=currency)
    log.debug('Raw data columnar from {} analysed'.format(file_type_processed))

    return d.orders_summary()


def analyse_orders_from_file_row(file_path: str, z_value: Decimal, reorder_cost: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = "month", length: int = 12, currency: str = 'USD') -> list:
    """ Analyse multiple SKUs from a file with data arranged by row.

    Args:
        file_path (file):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.
        length (int):           The length of the period.

    Returns:
        list:       A list of summaries containint

    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    Examples:
    >>> from supplychainpy.model_inventory import analyse_orders_from_file_row
    >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
    >>> analysed_data = analyse_orders_from_file_row(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
    ...                                                     reorder_cost=Decimal(45),
    ...                                                     z_value=Decimal(1.28),
    ...                                                     file_type="csv",
    ...                                                     retail_price=Decimal(30),
    ...                                                     currency='USD')




    """
    warnings.warn('Analyse orders function has been deprecated. Please use the analyse function', DeprecationWarning)
    orders = {}
    analysed_orders_summary = []
    analysed_orders_collection = []
    item_list = {}
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

            if quantity_on_hand is None:
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
    """
    Analyse orders data from file and returns ABCXYZ analysis

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (str):        The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        length (int):           The number of periods in the data-ser referenced from the second column of the row
                                onwards.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.
        currency (str):

    Returns:
        list:     An AbcXyz class object is returned.

    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    Examples:

    >>> from decimal import Decimal
    >>> from supplychainpy.model_inventory import analyse_orders_from_file_col
    >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
    >>> abc = analyse_orders_abcxyz_from_file(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
    ...                                                          z_value=Decimal(1.28),
    ...                                                          reorder_cost=Decimal(5000),
    ...                                                          file_type="csv")

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
        if quantity_on_hand is None:
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

        AbcXyz(analysed_orders_collection)

    return analysed_orders_collection


def recommendations(analysed_orders: UncertainDemand, forecast: dict) -> dict:
    """ Generate Recommendations for each SKU and the inventory Profile.

    Args:
        analysed_orders (UncertainDemand):  UncertainDemand object of analysed orders.
        forecast (dict):                    Output from a Forecast.

    Returns:
        dict:   Returns recommendations for each sku and for the inventory profile.

    Examples:
    >>> from decimal import Decimal
    >>> from supplychainpy.sample_data.config import ABS_FILE_PATH
    >>> from supplychainpy.model_inventory import analyse
    >>> from supplychainpy.model_inventory import recommendations
    ...
    >>> analysed_order = analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
    ...                                        z_value=Decimal(1.28),
    ...                                          reorder_cost=Decimal(5000),
    ...                                          file_type="csv", length=12,currency='USD')
    ...
    >>> holts_forecast = {analysis.sku_id: analysis.holts_trend_corrected_forecast for analysis in
    ...                     analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'], z_value=Decimal(1.28),
    ...                                          reorder_cost=Decimal(5000), file_type="csv",
    ...                                          length=12,currency='USD')}
    ...
    >>> recommend = recommendations(analysed_orders=analysed_order, forecast=holts_forecast)
    """

    recommend = {'sku_recommendations': run_sku_recommendation(analysed_orders=analysed_orders, forecast=forecast),
                 'profile_recommendations': run_profile_recommendation(analysed_orders=analysed_orders, forecast=forecast),
                 }

    return recommend


def summarise(analysed_orders: UncertainDemand):
    pass

# the np method allows a numpy array to be used. This requires the specification of a period and length the data is
# supposed to cover. This method also allows the use of lead time arrays for calculating average leadtimes. There
# also be an analyse_orders_from_file_np. using the analyse_orders_np method to process each row.

# def analyse_orders_np(unit_cost: Decimal, period: np.array, z_value: Decimal, orders: np.array,
#                      lead_time_np: np.array = [],
#                      lead_time: Decimal = 0.00, length: int = 12) -> dict:
#    d = analyse_uncertain_demand.UncertainDemandNp(orders_np=orders, length=length, period=period)
#    d.print_period()
