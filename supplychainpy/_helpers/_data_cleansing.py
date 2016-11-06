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
from decimal import Decimal
from warnings import warn
import csv
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

TABLE_HEADINGS = {
    'UNIT_COST': 'unit_cost',
    'LEAD_TIME': 'lead_time',
    'RETAIL_PRICE': 'retail_price',
    'QUANTITY_ON_HAND': 'quantity_on_hand',
    'BACKLOG': 'backlog'
}

# TODO-feature format pandas frame
# TODO-feature allow data munger to accept any delimiter as a parameter
def clean_orders_data_col_txt(file) -> dict:
    """

    Args:
        file:

    Returns:
        dict:
    """
    item_list = {}
    split_line = []
    for line in file:
        split_line.append(line.split("|"))
    for item in split_line:
        item_list[item[0]] = Decimal(item[1].strip())
    return item_list


# TODO-feature make csv version of clean_orders also take into account column number add tests (create csv file)
def clean_orders_data_col_csv(file) -> dict:
    item_list = {}
    read_csv = csv.reader(file)
    headers = next(read_csv)
    split_line = list(read_csv)
    for item in split_line:
        item_list[item[0]] = Decimal(item[1])
    return item_list


# TODO-feature allow data munger to accept any delimiter as a parameter
def clean_orders_data_row(file, length: int) -> dict:
    collection = []
    try:
        sku_list = []
        split_line = []
        composite = {}

        # unpacks the line form the txt file and splits using delimiter (default pipe) to split_line list
        for line in file:
            split_line.append(line.split("|"))
        # sorts all parts of the list into labeled dictionary
        for row in split_line:
            for index, item in enumerate(row):
                if int(index) < 1:
                    composite["sku_id"] = item
                elif 1 <= int(index) <= length:
                    sku_list.append(item.strip("\n"))
                elif int(index) == length + 1:
                    composite["unit_cost"] = item.strip("\n")
                elif int(index) == length + 2:
                    composite["lead_time"] = item.strip("\n")
                    # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                    # and throw an exception.
                    composite["demand"] = sku_list
                    sku_list = []
                    collection.append(composite)
                    composite = {}
    except OSError:
        print("")

    return collection


# TODO-feature cleans a text or csv file and insert into numpy array
# remember to specify in documentation that the orders data will assume 12 months unless otherwise stated
def clean_orders_data_row_csv(file, length: int = 12) -> dict:
    # check length of list, check length of the length specified and validate the length and make sure it is long enough
    # to support the unit_cost, lead_time, asp, quantity_on_hand
    collection = []
    try:

        sku_list = []
        composite = {}

        read_csv = csv.reader(file)
        headers = next(read_csv)
        split_line = list(read_csv)

        for row in split_line:
            if length == len(row) - 6:
                for index, item in enumerate(row):
                    if int(index) < 1:
                        composite["sku_id"] = item
                    elif 1 <= index <= length:
                        sku_list.append(item)
                    elif index == length + 1:
                        composite["unit_cost"] = item
                        log.info("Extracted unit cost for sku. SKU: {} UNIT COST: {} ".format(
                            composite.get("sku_id", "UNKNOWN_SKU"), item))
                    elif index == length + 2:
                        composite["lead_time"] = item
                        log.info("Extracted unit cost for sku. SKU: {} LEAD-TIME: {} ".format(
                            composite.get("sku_id", "UNKNOWN_SKU"), item))
                    elif index == length + 3:
                        composite["retail_price"] = item
                        log.info("Extracted unit cost for sku. SKU: {}  RETAIL PRICE: {} ".format(
                            composite.get("sku_id", "UNKNOWN_SKU"), item))
                    elif index == length + 4:
                        composite["quantity_on_hand"] = item
                        log.info("Extracted unit cost for sku. SKU: {} QUANTITY ON HAND: {} ".format(
                            composite.get("sku_id", "UNKNOWN_SKU"), item))
                    elif index == length + 5:
                        composite["backlog"] = item
                        log.info("Extracted unit cost for sku. SKU: {} BACKLOG: {} ".format(
                            composite.get("sku_id", "UNKNOWN_SKU"), item))
                        # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                        # and through an exception.
                composite["demand"] = tuple(sku_list)
                composite["headers"] = headers
                sku_list = []

                if composite.get("sku_id") is None or composite.get("unit_cost") is None or composite.get("lead_time") is \
                        None or composite.get("retail_price") is None:
                    err_msg = "csv file is formatted incorrectly. Please make sure the  formatted file\n [sku_id," \
                              " orders1,orders2....unit_cost, lead_time, retail_price, quantity_on_hand"
                    raise Exception(err_msg)

                collection.append(composite)
                composite = {}
            else:
                formatting_err = "The file formatting is incorrect. The specified column count supplied as a" \
                                 " parameter is {}.\n Including the sku_id, unit_cost, lead_time, retail_price\n " \
                                 "and quantity on hand the csv row should be {} columns long.\n The current" \
                                 " column count is {}. Please check the file or specified length."
                raise Exception(formatting_err.format(length, (length + 1) + len(TABLE_HEADINGS), len(row)))
    except OSError as e:
        print(e)

    return collection

def match_headers(headers: list)->dict:
    pass

def check_extension(file_path, file_type: str) -> bool:
    """ Check the correct file type has been selected.

    Args:
        file_path (file):   The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        file_type (str):    specifying 'csv' or 'text'
    Returns:
        bool:   Extension present or not.

    """
    try:
        if file_path.endswith(".txt") and file_type.lower() == "text":
            flag = True
        elif file_path.endswith(".csv") and file_type.lower() == "csv":
            flag = True
        else:
            flag = False
        return flag
    except AttributeError as e:
        print(e)


# refocator length to column count
# if a user specifies a lower column_count than actually supplied then the oher columns are going to be incorrect.
# probably best to check heading using regx
