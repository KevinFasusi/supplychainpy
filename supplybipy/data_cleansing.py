from decimal import Decimal


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
    collection = []

    for line in file:
        split_line.append(line.split("|"))
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
                # and through an exception.
                composite["orders"] = sku_list
                sku_list = []
                collection.append(composite)
                composite = {}
    return collection
