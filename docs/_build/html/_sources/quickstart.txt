Quick Guide
===========

The following guide assumes that the supplychainpy library has already been installed. If not please use the
instructions for :ref:`Installation`.

While the supplychainpy library can be used in any way you deem fit, the library was created to assist a workflow that
is reliant on Excel, Excel formulas and VBA. Below we go through the use cases and implementations specific to the
domain (supply chain, operations and manufacturing).

Summarising Inventory
---------------------

A quick example of a typical inventory analysis takes several formulas, manual processes or pivot tables and in
some cases vba to achieve. With supplychainpy the same analysis can be achieved in 10 lines of code
(**only 3 lines of code** for the analysis and another 7 to get the results into Excel). In the example below supplying
a `dict` of "Orders" data-points can generate a summary that includes:

- demand variability
- reorder level
- safety stock
- reorder quantities ...

.. code:: python

    >>> from supplychainpy import model_inventory
    >>> yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75,
    >>>                 'may': 75, 'jun': 75, 'jul': 25,'aug': 25,
    >>>                 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    >>> summary = model_inventory.analyse_orders(data_set= yearly_demand,
    >>>                                          sku_id='RX983-90',
    >>>                                          lead_time=Decimal(3), unit_cost=Decimal(34.99),
    >>>                                          reorder_cost=Decimal(400),z_value=Decimal(1.28)
    >>> print(summary)

Currently the lead-time and the yearly_demand must be in the same units (the user has to make the correct conversion).
This will be changing soon.

.. parsed-literal::

    {'standard_deviation': '25',
        'demand_variability': '0.500', 'sku': 'RX983-90',
	    'reorder_level': '142', 'average_order': '50',
	    'safety_stock': '55', 'economic_order_variable_cost': '0.00',
	    'revenue': '30594.00', 'reorder_quantity': '56'}

The same analysis can be made by supplying a pre-formatted `.csv` or `.txt`:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="text")
    >>> for sku in abc.orders
    >>>     print ('Sku: {} Economic Order Quantity: {} Sku Revenue: {} ABCXYZ Classification: {}'
    >>>            .format(sku.sku_id sku.economic_order_qty, sku.revenue, sku.abcxyz_classification)


Using openpyxl or xlwings this analysis can be placed in a worksheet or used in further calculations. Below is an
xlwings example:

.. code:: python

    >>> from xlwings import Workbook, Range
    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> wb = Workbook(r'~/Desktop/test.xlsx'), Range
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28), reorder_cost=Decimal(5000), file_type="csv")
    >>> x = 1
    >>> for sku in abc.orders:
    >>>     Range('A'+ str(x)).value = sku.sku_id
    >>>     Range('B' + str(x)).value = float(sku.economic_order_qty)
    >>>     Range('C' + str(x)).value = float(sku.revenue)
    >>>     Range('D' + str(x)).value = sku.abcxyz_classification
    >>>     +=1

The columns A-D will now be populated with the values below:




Where to go from here?
======================

While the library is currently in development there are several ways the current functionality can be extended:

Filtering
---------
Using python list comprehensions or yield to filter in comparison to using pivot tables.

Further Analysis
----------------


Features in development
=======================



You are more than a filthy sheet spreader!
------------------------------------------

Much maligned but an essential tool

