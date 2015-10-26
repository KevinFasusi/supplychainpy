from decimal import *


def clean_orders_data_col(file):
    item_list = {}
    split_line = []
    for line in file:
        split_line.append(line.split("|"))
    for item in split_line:
        item_list[item[0]] = Decimal(item[1].strip())
    return item_list


def clean_orders_data_row(file):
    sku_list = []
    split_line = []
    composite = {}
    for line in file:
        split_line.append(line.split("|"))
    for row in split_line:
        for item in range(len(row)):
            if item < 1:
                sku_id = row[item]
            else:
                sku_list.append(row[item].strip("\n"))
            if item == 12:
                # if the sku id is not unique the the data will just append. Need to check if there are duplicates
                # and through an exception.
                composite[sku_id] = sku_list
                sku_list = []
    return composite
