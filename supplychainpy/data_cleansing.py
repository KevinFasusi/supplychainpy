from decimal import Decimal
import csv


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
def clean_orders_data_row(file) -> dict:
    sku_list = []
    split_line = []
    composite = {}
    collection = []
    # unpacks the line form the txt file and splits using delimiter (default pipe) to split_line list
    for line in file:
        split_line.append(line.split("|"))
    # sorts all parts of the list into labeled dictionary
    for row in split_line:
        for item in range(len(row)):
            if item < 1:
                composite["sku id"] = row[item]
            elif 1 <= item <= 12:
                sku_list.append(row[item].strip("\n"))
            elif item == 13:
                composite["unit cost"] = row[item].strip("\n")
            elif item == 14:
                composite["lead time"] = row[item].strip("\n")
                # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                # and throw an exception.
                composite["demand"] = sku_list
                sku_list = []
                collection.append(composite)
                composite = {}
    return collection


# TODO-feature cleans a text or csv file and insert into numpy array
# remember to specify in documentation that the orders data will assume 12 months unless otherwise stated
def clean_orders_data_row_csv(file, length: int = 12) -> dict:
    sku_list = []
    composite = {}
    collection = []
    read_csv = csv.reader(file)
    headers = next(read_csv)
    split_line = list(read_csv)

    for row in split_line:
        for item in range(len(row)):
            if item < 1:
                composite["sku id"] = row[item]
            elif 1 <= item <= length:
                sku_list.append(row[item])
            elif item == length + 1:
                composite["unit cost"] = row[item]
            elif item == length + 2:
                composite["lead time"] = row[item]
                # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                # and through an exception.
                composite["demand"] = sku_list
                sku_list = []
                collection.append(composite)
                composite = {}
    return collection
