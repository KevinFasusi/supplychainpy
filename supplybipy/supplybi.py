from supplybipy.build_model import model_orders, analyse_orders_from_file_col, analyse_orders_from_file_row

__author__ = 'kevin'


def main():
    r = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
         'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}

    summary = model_orders(r, 'RX983-90', 3, 50.99, 400, 1.28)
    print(summary)

    summary = analyse_orders_from_file_col('test.txt', 'RX9887-90', 4, 45, 400, 1.28)
    print(summary)

    big_summary = analyse_orders_from_file_row('test_row.txt', 1.28, 400)
    print(big_summary)



if __name__ == '__main__': main()
