[![Build Status](https://travis-ci.org/KevinFasusi/supplychainpy.svg?branch=master)](https://travis-ci.org/KevinFasusi/supplychainpy?branch=master)

#Supplychainpy

Supplychainpy is a Python library for supply chain analysis, modeling and simulation. Use in conjunction with popular
data analysis libraries and tools such as xlwings or data nitro (for Excel spreadsheet applications), pandas,
numpy, matplotlib, ipython and Jupyters for a powerful supply chain data analysis toolchain.

The library is currently in early stages of development, so not ready for use in production. However some fun can be had
by passing a csv or text file in the correct format and outputting inventory analysis such as:
- economic order quantities
- safety stock
- abc xyz classification
- demand variability
- ...


without having to write several formulas excel, use VBA or manual processes that do not scale. This functionality is
scalable and can be achieved in about 10 lines of code.

##Quick Install

The easiest way to install supplychainpy is via pip: 'pip install supplychainpy'

##Dependencies

##Quick Guide
1. Fire up the python interpreter or `ipython notebook` from the command line.
2. Format the `.csv` or `.txt`.e.g `sku id`, `order1`, `order2`,... `orders12`, `lead time`, `unit cost`
At the moment the lead-time must match the orders time bucket i.e both should be in days, weeks or months. This will
change promptly.


```python
	from xlwings import Workbook, Range
    from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    wb = Workbook(r'~/Desktop/test.xlsx'), Range
    abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value= 1.28, reorder_cost=5000, file_type="csv")
    x = 1
    for sku in abc.orders:
        Range('A'+ str(x)).value = sku.sku_id
        Range('B' + str(x)).value = float(sku.economic_order_qty)
        Range('C' + str(x)).value = float(sku.revenue)
        Range('D' + str(x)).value = sku.abcxyz_classification
        x +=1
```


Documentation:

Website:

youtube:



