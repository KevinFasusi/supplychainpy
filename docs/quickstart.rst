Quick Guide
===========
.. note::

    All profiling has been carried out on the following system:

    +------------+------------------------------------+
    | Component  |               Spec.                |
    +============+====================================+
    |    CPU     | Xeon 1650v3 (15M Cache, 3.50 GHz)  |
    +------------+------------------------------------+
    |    Ram     | 32gb ddr4 2133                     |
    +------------+------------------------------------+
    |   ssd      | m.2 Samsung                        |
    +------------+------------------------------------+
    |   gpu      | GTX 980ti CUDA cores 2816 1000MHz  |
    +------------+------------------------------------+

While the supplychainpy library can be used in any way you deem fit, the library was created to assist a workflow that
is reliant on Excel, Excel formulas and VBA. Below we go through the use cases and implementations specific to the
domain (supply chain, operations and manufacturing).

The following guide assumes that the supplychainpy library has already been installed. If not please use the
instructions for :ref:`Installation`.

Inventory Analysis
------------------

A quick example of a typical inventory analysis takes several formulas, manual processes or pivot tables and in
some cases vba to achieve. Using the supplychainpy library can reduce the time and effort taken for the same analysis.
In the example below supplying a `dict` of "Orders" data-points can generate a summary that includes:

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

Time taken in seconds: 0.0008091926574707031.


Currently the lead-time and the yearly_demand must be in the same units (the user has to make the correct conversion).
This will be changing soon.
.. parsed-literal::

    {'average_order': '50',
    'safety_stock': '55',
    'sku': 'RX983-90',
    'reorder_level': '142',
    'reorder_quantity': '67',
    'revenue': '20994.00',
    'demand_variability': '0.499',
    'standard_deviation': '24'}

The same analysis can be made by supplying a pre-formatted `.csv` or `.txt`:

.. parsed-literal::

    Sku,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,unit cost,lead-time
    KR202-209,1509,312,88,1261,1231,2598,968,427,2927,2707,731,2598,400,2
    KR202-210,1006,206,2588,670,2768,2809,1475,1537,919,2525,440,2691,394,2
    KR202-211,1840,2284,850,983,2737,1264,2002,1980,235,1489,218,525,434,4
    KR202-212,104,2262,350,528,2570,1216,1101,2755,2856,2381,1867,2746,474,3
    KR202-213,489,954,1112,199,919,330,561,2372,921,1587,1532,1512,514,1

A file named `data.csv` can be used to generate the same analysis in `dict` based example. The full file is supplied in
the installation folder. The example below generates the result for 32 skus.

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> print (abc.abcxyz_summary)


Time taken in seconds:0.009269237518310547.

.. parsed-literal::


    [{'AX': 0}, {'AY': 14}, {'AZ': 7}, {'BX': 0}, {'BY': 3}, {'BZ': 2}, {'CX': 0}, {'CY': 3}, {'CZ': 3}]


.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> for sku in abc.orders:
    >>>     print('Sku: {} Economic Order Quantity: {:.0f} Sku Revenue: {:.0f} ABCXYZ Classification: {}'.format(sku.sku_id,
    >>>                                                 sku.economic_order_qty, sku.revenue, sku.abcxyz_classification))

Time taken in seconds: 0.009444236755371094.

.. parsed-literal::

    Sku: KR202-209 Economic Order Quantity: 1311 Sku Revenue: 6942800 ABCXYZ Classification: CZ
    Sku: KR202-210 Economic Order Quantity: 1405 Sku Revenue: 7900000 ABCXYZ Classification: CY
    Sku: KR202-211 Economic Order Quantity: 1224 Sku Revenue: 6900000 ABCXYZ Classification: CZ
    Sku: KR202-212 Economic Order Quantity: 1317 Sku Revenue: 10000000 ABCXYZ Classification: BY
    Sku: KR202-213 Economic Order Quantity: 981 Sku Revenue: 6700000 ABCXYZ Classification: CY
    Sku: KR202-214 Economic Order Quantity: 1170 Sku Revenue: 10000000 ABCXYZ Classification: BY
    Sku: KR202-215 Economic Order Quantity: 1030 Sku Revenue: 9500000 ABCXYZ Classification: CY
    Sku: KR202-216 Economic Order Quantity: 1054 Sku Revenue: 11000000 ABCXYZ Classification: BY
    Sku: KR202-217 Economic Order Quantity: 1083 Sku Revenue: 13000000 ABCXYZ Classification: AY
    Sku: KR202-218 Economic Order Quantity: 862 Sku Revenue: 9300000 ABCXYZ Classification: CZ
    Sku: KR202-219 Economic Order Quantity: 894 Sku Revenue: 11000000 ABCXYZ Classification: BZ
    Sku: KR202-220 Economic Order Quantity: 967 Sku Revenue: 15000000 ABCXYZ Classification: AY
    Sku: KR202-221 Economic Order Quantity: 937 Sku Revenue: 15000000 ABCXYZ Classification: AY
    Sku: KR202-222 Economic Order Quantity: 848 Sku Revenue: 13000000 ABCXYZ Classification: AZ
    Sku: KR202-223 Economic Order Quantity: 932 Sku Revenue: 19000000 ABCXYZ Classification: AY
    Sku: KR202-224 Economic Order Quantity: 863 Sku Revenue: 17000000 ABCXYZ Classification: AY
    Sku: KR202-225 Economic Order Quantity: 960 Sku Revenue: 23000000 ABCXYZ Classification: AY
    Sku: KR202-226 Economic Order Quantity: 715 Sku Revenue: 13000000 ABCXYZ Classification: BZ
    Sku: KR202-227 Economic Order Quantity: 861 Sku Revenue: 21000000 ABCXYZ Classification: AY
    Sku: KR202-228 Economic Order Quantity: 794 Sku Revenue: 20000000 ABCXYZ Classification: AZ
    Sku: KR202-229 Economic Order Quantity: 722 Sku Revenue: 17000000 ABCXYZ Classification: AY
    Sku: KR202-230 Economic Order Quantity: 838 Sku Revenue: 24000000 ABCXYZ Classification: AY
    Sku: KR202-231 Economic Order Quantity: 771 Sku Revenue: 21000000 ABCXYZ Classification: AZ
    Sku: KR202-232 Economic Order Quantity: 815 Sku Revenue: 25000000 ABCXYZ Classification: AY
    Sku: KR202-233 Economic Order Quantity: 654 Sku Revenue: 18000000 ABCXYZ Classification: AZ
    Sku: KR202-234 Economic Order Quantity: 631 Sku Revenue: 18000000 ABCXYZ Classification: AY
    Sku: KR202-235 Economic Order Quantity: 810 Sku Revenue: 31000000 ABCXYZ Classification: AY
    Sku: KR202-236 Economic Order Quantity: 622 Sku Revenue: 22000000 ABCXYZ Classification: AZ
    Sku: KR202-237 Economic Order Quantity: 671 Sku Revenue: 27000000 ABCXYZ Classification: AZ
    Sku: KR202-238 Economic Order Quantity: 685 Sku Revenue: 27000000 ABCXYZ Classification: AY
    Sku: KR202-239 Economic Order Quantity: 713 Sku Revenue: 31000000 ABCXYZ Classification: AY
    Sku: KR202-240 Economic Order Quantity: 680 Sku Revenue: 27000000 ABCXYZ Classification: AZ

Using openpyxl or xlwings this analysis can be placed in a worksheet or used in further calculations. Below is an
xlwings example:

.. code:: python

	>>> from xlwings import Workbook, Range
	>>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
	>>> wb = Workbook(r'~/Desktop/test.xlsx'), Range
	>>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value= Decimal(1.28), reorder_cost=Decimal(5000), file_type="csv")
	>>>
	>>> for index, sku in enumerate(abc.orders):
	>>>     Range('A'+ str(index)).value = sku.sku_id
	>>>     Range('B' + str(index)).value = float(sku.economic_order_qty)
	>>>     Range('C' + str(index)).value = float(sku.revenue)
	>>>     Range('D' + str(index)).value = sku.abcxyz_classification

The columns A-D will now be populated with the values below:

Monte Carlo simulation
----------------------

The code below returns the `transaction report` covering the number of periods specified, multiplied by the number of runs
requested. The higher the number of runs the more accurately the simulation captures the dynamics of the system limited by
the assumptions inherent in the simulations design.

.. code:: python

    >>> from supplychainpy import simulate
    >>> sim = simulate.run_monte_carlo(file_path="data.csv", z_value=Decimal(1.28), runs=1,
    >>>                               reorder_cost=Decimal(4000), file_type="csv", period_length=12)
    >>> for sku in sim:
    >>>     print(sku)

This is the output from 1 run for 1 sku over a period of 12 months. The demand is a normal random distribution
and then years worth of transactions are simulated, the results are below.

.. parsed-literal::

    [{'delivery': '0', 'quantity_sold': '1354', 'po_received': '', 'po_quantity': '3630', 'opening_stock': '1446',
    'shortage_units': '0', 'closing_stock': '1355', 'revenue': '541946', 'demand': '92', 'index': '1', 'po_raised':
    'PO 31', 'period': '1', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '1354', 'po_received': '', 'po_quantity': '6268', 'opening_stock': '1355',
    'shortage_units': '1283', 'closing_stock': '0', 'revenue': '541946', 'demand': '2638', 'index': '1', 'po_raised':
    'PO 41', 'period': '2', 'backlog': '1283', 'sku_id': 'KR202-209', 'shortage_cost': '154032'}]
    [{'delivery': '3630', 'quantity_sold': '1520', 'po_received': 'PO 31', 'po_quantity': '3464', 'opening_stock': '0',
    'shortage_units': '0', 'closing_stock': '2805', 'revenue': '608381', 'demand': '826', 'index': '1', 'po_raised':
    'PO 51', 'period': '3', 'backlog': '1283', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '6269', 'quantity_sold': '7753', 'po_received': 'PO 41', 'po_quantity': '0', 'opening_stock': '2805',
    'shortage_units': '0', 'closing_stock': '7754', 'revenue': '3101401', 'demand': '1320', 'index': '1',
    'po_raised': '', 'period': '4', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '3464', 'quantity_sold': '10203', 'po_received': 'PO 51', 'po_quantity': '0', 'opening_stock': '7754',
    'shortage_units': '0', 'closing_stock': '10204', 'revenue': '4081460', 'demand': '1014', 'index': '1',
    'po_raised': '', 'period': '5', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '8926', 'po_received': '', 'po_quantity': '0', 'opening_stock': '10204',
    'shortage_units': '0', 'closing_stock': '8927', 'revenue': '3570654', 'demand': '1277', 'index': '1',
    'po_raised': '','period': '6', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '7284', 'po_received': '', 'po_quantity': '0', 'opening_stock': '8927',
    'shortage_units': '0', 'closing_stock': '7285', 'revenue': '2913927', 'demand': '1642', 'index': '1',
    'po_raised': '','period': '7', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '6387', 'po_received': '', 'po_quantity': '0', 'opening_stock': '7285',
    'shortage_units': '0', 'closing_stock': '6387', 'revenue': '2554819', 'demand': '898', 'index': '1',
    'po_raised': '','period': '8', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '4708', 'po_received': '', 'po_quantity': '276', 'opening_stock': '6387',
    'shortage_units': '0', 'closing_stock': '4709', 'revenue': '1883461', 'demand': '1678', 'index': '1', 'po_raised':
    'PO 111', 'period': '9', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '0', 'quantity_sold': '2954', 'po_received': '', 'po_quantity': '2030', 'opening_stock': '4709',
    'shortage_units': '0', 'closing_stock': '2955', 'revenue': '1181806', 'demand': '1754', 'index': '1', 'po_raised':
    'PO 121', 'period': '10', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '276', 'quantity_sold': '674', 'po_received': 'PO 111', 'po_quantity': '4310',
    'opening_stock': '2955', 'shortage_units': '0', 'closing_stock': '674', 'revenue': '269654', 'demand': '2557',
    'index': '1', 'po_raised': 'PO 131', 'period': '11', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]
    [{'delivery': '2031', 'quantity_sold': '947', 'po_received': 'PO 121', 'po_quantity': '4037',
    'opening_stock': '674', 'shortage_units': '0', 'closing_stock': '947', 'revenue': '378903', 'demand': '1757',
    'index': '1', 'po_raised': 'PO 141', 'period': '12', 'backlog': '0', 'sku_id': 'KR202-209', 'shortage_cost': '0'}]


The monte carlo analysis calls the `model_inventory.analyse_orders_abcxyz_from_file` method to use the historical
analysis for the simulation. The `monte_carlo.SetupMonteCarlo` class is used to call the `generate_normal_random_distribution`
method.

Currently the quantity raised on the po in the above analysis is calculated using a calculation provided in the :ref:`calculations`
sections. In release 0.0.3 this will be updated to a user selected forecast method. The current monte carlo anlysis is
is missing the declaration of a parameter to optimise. This feature will also arrive in release 0.0.3.

After running the monte carlo simulation, the results can be passed as a parameter for summary:

    # i = simulate.summarize_window(simulation_frame=sim, period_length=12)
    # for r in i:
    #     print(r)