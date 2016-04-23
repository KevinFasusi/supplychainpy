from decimal import Decimal
import re
import csv


# TODO-feature format pandas frame
# TODO-feature allow data munger to accept any delimiter as a parameter
def clean_orders_data_col_txt(file) -> dict:
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
    try:
        sku_list = []
        split_line = []
        composite = {}
        collection = []
        # unpacks the line form the txt file and splits using delimiter (default pipe) to split_line list
        for line in file:
            split_line.append(line.split("|"))
        # sorts all parts of the list into labeled dictionary
        for row in split_line:
            for index, item in enumerate(row):
                if int(index) < 1:
                    composite["sku id"] = item
                elif 1 <= int(index) <= length:
                    sku_list.append(item.strip("\n"))
                elif int(index) == length + 1:
                    composite["unit cost"] = item.strip("\n")
                elif int(index) == length + 2:
                    composite["lead time"] = item.strip("\n")
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
    try:

        sku_list = []
        composite = {}
        collection = []
        read_csv = csv.reader(file)
        headers = next(read_csv)
        split_line = list(read_csv)

        for row in split_line:
            if length == len(row) - 5:
                for index, item in enumerate(row):
                    if int(index) < 1:
                        composite["sku id"] = item
                    elif 1 <= int(index) <= length:
                        sku_list.append(item)
                    elif int(index) == length + 1:
                        composite["unit cost"] = item
                    elif int(index) == length + 2:
                        composite["lead time"] = item
                    elif int(index) == length + 3:
                        composite["retail_price"] = item
                    elif int(index) == length + 4:
                        composite["quantity_on_hand"] = item
                        # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                        # and through an exception.
                composite["demand"] = sku_list
                sku_list = []

                if composite.get("sku id") is None or composite.get("unit cost") is None or composite.get("lead time") is \
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
                                 " column count  is {}. Please check the file or specified length."
                raise Exception(formatting_err.format(length, length + 5, len(row)))
    except OSError:
        print("check")

    return collection


# refocator length to column count
# if a user specifies a lower column_count than actually supplied then the oher columns are going to be incorrect.
# probably best to check heading using regx
