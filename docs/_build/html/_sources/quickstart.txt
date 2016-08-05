Quick Guide
===========

.. warning::
    The library is currently under development and in planning stages. The library should not be used in
    production at this time.


.. note::

    All profiling has been carried out on the following systems:

    +------------+------------------------------------+------------------+--------------------------+
    | system     |           CPU                      | Ram              |  OS                      |
    +============+====================================+==================+==========================+
    |   PC       | Xeon 1650v3 (15M Cache, 3.50 GHz)  | 32gb ddr4 2133   | linux (xubuntu, windows) |
    +------------+------------------------------------+------------------+--------------------------+
    | Macbook Air|            i7-4650U                |   8gb ddr3 1600  | OS X (yosemite)          |
    +------------+------------------------------------+------------------+--------------------------+

    Timings are provided as simple benchmarks and will vary based on system and current load.
    The computations here are mainly cpu bound, io may be a factor when reading from file (csv txt).

Overview
--------

Supplychainpy is a Python library for supply chain analysis, modeling and simulation. Using supplychainpy
with modern data analysis libraries and tools such as Xlwings or Data Nitro (for Excel spreadsheet applications),
Pandas, NumPy, Matplotlib, Ipython and Jupyter makes for a powerful supply chain data analysis toolchain.

The library was created to assist a workflow that is reliant on Excel, Excel formulas and VBA. Below we go through the use cases and implementations particular to the
domain (supply chain, operations and manufacturing).

This quick guide is skewed towards analysts with the requisite domain knowledge, who predominantly use Excel. Some
knowledge of Python or programming is assumed, although those new to data analysis or using Python will likely be able to
follow with assistance from other material.

The following guide assumes that the supplychainpy library has already been installed. If not, please use the
instructions for :ref:`installation`.

Inventory Analysis
------------------

A quick example of a typical inventory analysis takes several formulas, manual processes or pivot tables and in
some cases VBA to achieve. Using the supplychainpy library can reduce the time taken and effort made for the same analysis.
In the example below supplying a dictionary of "Orders" data-points can generate a summary.

.. code:: python

    >>> from supplychainpy import model_inventory
    >>> yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75,
    >>>                 'may': 75, 'jun': 75, 'jul': 25,'aug': 25,
    >>>                 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    >>> summary = model_inventory.analyse_orders(self._yearly_demand,  sku_id='RX983-90', lead_time= Decimal(3),
    >>>                                             unit_cost=Decimal(50.99), reorder_cost=Decimal(400),
    >>>                                             z_value=Decimal(1.28), retail_price=Decimal(600), quantity_on_hand=Decimal(390)))
    >>> print(summary)

Excess and shortages are now available.

.. parsed-literal::

    {'standard_deviation': '25',
    'safety_stock': '55',
    'excess_stock': '161',
    'revenue': '360000.00',
    'reorder_level': '142',
    'demand_variability': '0.500',
    'shortages': '0',
    'reorder_quantity': '56',
    'sku': 'RX983-90',
    'average_order': '50'}

Currently the `lead_time` and the `yearly_demand` parameters, must be in the same units (the user must make the correct conversion).
This will be changing soon.



.. note::  The required format has changed moving from release-0.0.3 to release-0.0.4. **Retail price** and **quantity on hand** have are required.

The same analysis can be made by supplying a pre-formatted `.csv` or `.txt`:

.. parsed-literal::

    Sku,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,unit cost,lead-time,retail_price,quantity_on_hand
    KR202-20,1509,312,88,1261,1231,2598,968,427,2927,2707,731,2598,400,2,900,1003
    KR202-210,1006,206,2588,670,2768,2809,1475,1537,919,2525,440,2691,394,2,1300,3224
    KR202-211,1840,2284,850,983,2737,1264,2002,1980,235,1489,218,525,434,4,1200,390
    KR202-212,104,2262,350,528,2570,1216,1101,2755,2856,2381,1867,274983,6,474,3,10,390
    KR202-213,489,954,1112,199,919,330,561,2372,921,1587,1532,1512,514,1,2000,2095
    KR202-214,2416,2010,2527,1409,1059,890,2837,276,987,2228,1095,1396,554,2,1800,55
    KR202-215,403,1737,753,1982,2775,380,1561,1230,1262,2249,824,743,594,1,2500,4308

Getting the file into this format from a database source may require an ETL tool such as SSIS (for windows SQL server) or a stored procedure or SQL script.
A blog post will be dedicated to the ETL process asap.


A file named `data.csv`, supplied with this distribution (release 0.0.2 onwards) can be used to generate the
same analysis in `dict` based example. The example below generates the result for 32 stock keeping units (sku).

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> print (abc.abcxyz_summary)

.. note::  simplified ABC XYZ (pareto) summary.

.. parsed-literal::


    {'AX': 0, 'AY': 14, 'AZ': 7, 'BX': 0, 'BY': 3, 'BZ': 2, 'CX': 0, 'CY': 3, 'CZ': 3}

This analysis completed in:

     +-------+----------------------+
     | system| time (seconds)       |
     +=======+======================+
     |  PC   |0.015653133392333984  |
     +-------+----------------------+
     |  Mac  |0.02649521827697754   |
     +-------+----------------------+

The orders analysis can be retrieved by using:

.. code:: python


    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>>
    >>> orders_analysis = [analysis.orders_summary() for analysis in
    >>>                   model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
    >>>                                                                   reorder_cost=Decimal(5000), file_type="csv",
    >>>                                                                   length=12)]
    >>> print(orders_analysis)

output:

.. parsed-literal::

    {'unit_cost': '400', 'standard_deviation': '976', 'economic_order_quantity': '1311', 'ABC_XYZ_Classification': 'CZ',
    'safety_stock': '1767', 'reorder_level': '3812', 'demand_variability': '0.675', 'shortages': '4855', 'excess_stock': '0',
    'reorder_quantity': '380', 'revenue': '15621300', 'economic_order_variable_cost': '186365.16', 'sku': 'KR202-209', 
    'average_orders': '1446.4167'}, 

This analysis completed in:

     +-------+----------------------+
     | system| time (seconds)       |
     +=======+======================+
     |  PC   | 0.0178067684173584   |
     +-------+----------------------+
     |  Mac  | 0.024185895919799805 |
     +-------+----------------------+
     
Use the `describe_sku` method a retrieve a summary for a specific skus:

.. code::

    >>> from supplychainpy import model_inventory
    >>> from supplychainpy.inventory.summarise import OrdersAnalysis
    >>> analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
    >>>
    >>> for summarised in analysis_summary.describe_sku('KR202-217'):
    >>>     print(summarised)

The output for a sku description is different to the `oreders_summary` method for the whole analysis:

.. parsed-literal::

    {'shortage_units': '7245', 'retail_price': '5433', 'shortage_rank': '12', 'safety_stock_units': '1871', 
    'average_orders': '1664', 'min_order': '224', 'excess_units': '0', 'percentage_contribution_revenue': '0.021250938', 
    'gross_profit_margin': '4759', 'safety_stock_cost': '1261211.3', 'sku_id': 'KR202-217', 'classification': 'AY', 
    'excess_cost': '0', 'safety_stock_rank': '20', 'revenue_rank': '12', 'unit_cost': '674', 'revenue': '108480711', 
    'excess_rank': '13', 'markup_percentage': '7.0608309', 'max_order': '2987', 'shortage_cost': '4883130'}
    
The descriptive summary includes:

- shortage_rank
- min/max orders
- excess_units
- revenue_rank
- excess_rank
- average_orders
- gross_profit_margin
- markup_percentage
- max_order


The describe_sku method can take multiple parameters:

.. code::

    >>> from supplychainpy import model_inventory
    >>> from supplychainpy.inventory.summarise import OrdersAnalysis
    >>> analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
    >>> 
    >>> skus = ['KR202-209', 'KR202-210', 'KR202-211']
    >>>
    >>> skus_description = [summarised for summarised in analysis_summary.describe_sku(*skus)]
    >>> print(skus_description)
    
Or simply:

.. code::

    >>> from supplychainpy import model_inventory
    >>> from supplychainpy.inventory.summarise import OrdersAnalysis
    >>> analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
    >>> 
    >>> for summarised in analysis_summary.describe_sku('KR202-209', 'KR202-210', 'KR202-211'):
    >>>     print(summarised)

Output:

.. parsed-literal::


    [{'markup_percentage': '1.25', 'retail_price': '900', 'excess_units': '0', 'classification': 'CZ',
     'excess_cost': '0', 'safety_stock_cost': '706680.47', 'safety_stock_rank': '29', 'revenue_rank': '31',
     'sku_id': 'KR202-209', 'excess_rank': '6', 'safety_stock_units': '1767', 'gross_profit_margin': '500', 
     'shortage_rank': '18', 'percentage_contribution_revenue': '0.0030601503', 'revenue': '15621300', 
     'average_orders': '1446', 'shortage_units': '4855', 'shortage_cost': '1942000', 'unit_cost': '400', 
     'max_order': '2927', 'min_order': '88'}, 
     {'markup_percentage': '2.2994924', 'retail_price': '1300', 'excess_units': '0', 'classification': 'CY',
      'excess_cost': '0', 'safety_stock_cost': '677310.89', 'safety_stock_rank': '30', 'revenue_rank': '28', 
      'sku_id': 'KR202-210', 'excess_rank': '7', 
      'safety_stock_units': '1719', 'gross_profit_margin': '906', 'shortage_rank': '19', 
      'percentage_contribution_revenue': '0.0050000889', 'revenue': '25524200', 'average_orders': '1636', 
      'shortage_units': '0', 'shortage_cost': '0', 'unit_cost': '394', 'max_order': '2809', 'min_order': '206'}, 
     {'markup_percentage': '1.7649770', 'retail_price': '1200', 'excess_units': '0', 'classification': 'CY', 'excess_cost': '0',
      'safety_stock_cost': '876674.29', 'safety_stock_rank': '27', 'revenue_rank': '30', 'sku_id': 'KR202-211', 'excess_rank': '8',
      'safety_stock_units': '2020', 'gross_profit_margin': '766', 'shortage_rank': '17', 
      'percentage_contribution_revenue': '0.0038568790', 'revenue': '19688400', 'average_orders': '1367', 'shortage_units': '7099', 
      'shortage_cost': '3080966', 'unit_cost': '434', 'max_order': '2737', 'min_order': '218'}]


The example below filters the results based on an attribute, in this case `shortage cost` using the attribute name shortages:


.. code:: python

    >>> from supplychainpy.inventory.summarise import OrdersAnalysis
    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>>
    >>> orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
    >>>                                                                             z_value=Decimal(1.28),
    >>>                                                                             reorder_cost=Decimal(5000),
    >>>                                                                             file_type="csv",
    >>>                                                                             length=12)
    >>>
    >>> analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
    >>> 
    >>> top_ten_shortages = [item for item in analysis_summary.sku_ranking_filter(attribute="shortages", count=10, reverse=True)]
    >>> 
    >>> print(top_ten_shortages)
    

The results for `top_ten_shortages`:


.. parsed-literal::
    
    {'demand_variability': '0.409', 'unit_cost': '994', 'sku': 'KR202-225', 'revenue': '195934200', 'average_orders': '1925', 
    'standard_deviation': '787', 'ABC_XYZ_Classification': 'AY', 'reorder_level': '7181', 'economic_order_quantity': '960', 
    'shortages': '11474', 'reorder_quantity': '278', 'excess_stock': '0', 'safety_stock': '2466', 'economic_order_variable_cost': '338919.52'},
    {'demand_variability': '0.565', 'unit_cost': '474', 'sku': 'KR202-212', 'revenue': '207330', 'average_orders': '1727.75', 
    'standard_deviation': '976', 'ABC_XYZ_Classification': 'CY', 'reorder_level': '5156', 'economic_order_quantity': '1317',
    'shortages': '7759', 'reorder_quantity': '382', 'excess_stock': '0', 'safety_stock': '2164', 'economic_order_variable_cost': '221726.52'},
    {'demand_variability': '0.613', 'unit_cost': '1074', 'sku': 'KR202-227', 'revenue': '98847720', 'average_orders': '1674.25', 
    'standard_deviation': '1027', 'ABC_XYZ_Classification': 'BZ', 'reorder_level': '5177', 'economic_order_quantity': '861', 
    'shortages': '7587', 'reorder_quantity': '250', 'excess_stock': '0', 'safety_stock': '2277', 'economic_order_variable_cost': '328549.13'}, 
    {'demand_variability': '0.360', 'unit_cost': '1394', 'sku': 'KR202-235', 'revenue': '1372010500', 'average_orders': '1921.5833', 
    'standard_deviation': '691', 'ABC_XYZ_Classification': 'AY', 'reorder_level': '4861', 'economic_order_quantity': '810', 
    'shortages': '7339', 'reorder_quantity': '235', 'excess_stock': '0', 'safety_stock': '1532', 'economic_order_variable_cost': '401004.30'}, 
    {'demand_variability': '0.507', 'unit_cost': '674', 'sku': 'KR202-217', 'revenue': '108480711', 'average_orders': '1663.9167', 
    'standard_deviation': '844', 'ABC_XYZ_Classification': 'AY', 'reorder_level': '4753', 'economic_order_quantity': '1083', 
    'shortages': '7245', 'reorder_quantity': '314', 'excess_stock': '0', 'safety_stock': '1871', 'economic_order_variable_cost': '259467.97'}, 
    {'demand_variability': '0.577', 'unit_cost': '434', 'sku': 'KR202-211', 'revenue': '19688400', 'average_orders': '1367.25', 
    'standard_deviation': '789', 'ABC_XYZ_Classification': 'CY', 'reorder_level': '4754', 'economic_order_quantity': '1224', 
    'shortages': '7099', 'reorder_quantity': '355', 'excess_stock': '0', 'safety_stock': '2020', 'economic_order_variable_cost': '188736.92'}, 
    {'demand_variability': '0.618', 'unit_cost': '1594', 'sku': 'KR202-240', 'revenue': '73256997', 'average_orders': '1548.25', 
    'standard_deviation': '956', 'ABC_XYZ_Classification': 'CZ', 'reorder_level': '4802', 'economic_order_quantity': '680', 
    'shortages': '7094', 'reorder_quantity': '197', 'excess_stock': '0', 'safety_stock': '2120', 'economic_order_variable_cost': '384904.27'}, 
    {'demand_variability': '0.579', 'unit_cost': '634', 'sku': 'KR202-216', 'revenue': '53917641', 'average_orders': '1481.4167', 
    'standard_deviation': '858', 'ABC_XYZ_Classification': 'CY', 'reorder_level': '4467', 'economic_order_quantity': '1054', 
    'shortages': '6999', 'reorder_quantity': '306', 'excess_stock': '0', 'safety_stock': '1901', 'economic_order_variable_cost': '237449.51'} ... 
    
    
Available attributes:

- demand_variability
- economic_order_quantity
- average_order
- safety_stock
- standard_deviation
- reorder_level
- reorder_quantity
- revenue
- economic_order_quantity
- economic_order_variable_cost
- ABC_XYZ_Classification
- excess_stock
- shortages


Although `quantity_on_hand` is not a mandatory field, omitting will cause shortages to reflect the `reorder_level + the lead_time_demand`

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

Monte Carlo simulation
----------------------

After analysing the orders, the results for safety stock may not adequately calculate
the service level required. The complexity of the supply chain operation may include randomness an analytical model
does not capture. A simulation is useful for giving a dynamic view of a complex operation. The simulation replicates
some of the complexity of the system over time.

The code below returns a transaction report covering the number of periods specified, multiplied by the number of runs
requested. The higher the number of runs the more accurately the simulation captures the dynamics of the system,
when summarised later. The simulation is limited by the assumptions inherent in the simulations design (detailed in the
:ref:`calculations`).

To start we need to analyse the orders again like we did in the inventory analysis above:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> orders_analysis = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")

The orders are then passed as a parameter to the monte carlo simulation:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> from supplychainpy import simulate
    >>> orders_analysis = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>>
    >>> sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, file_path="data.csv", z_value=Decimal(1.28), runs=100,
    >>>                               reorder_cost=Decimal(4000), file_type="csv", period_length=12)
    >>> for transaction in sim:
    >>>     print(transaction)

The monte carlo simulation generates normally distributed random demand, based on the historic data.
The demand for each sku is then used in each period to model a probable transaction history. The
output below are the transactions for 1 sku over 12 periods for 100 runs (1 run is shown).

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

This analysis completed in:

     +-------+----------------------+
     | system| time (seconds)       |
     +=======+======================+
     |  PC   |   6.883291244506836  |
     +-------+----------------------+
     |  Mac  | 11.78481912612915    |
     +-------+----------------------+


After running the monte carlo simulation, the results can be passed as a parameter for summary:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> from supplychainpy import simulate
    >>> orders_analysis = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>>
    >>> sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, runs=100, period_length=12)
    >>>
    >>> sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)
    >>> for r in i:
    >>> 	print(r)

The result is a transactions summary for each SKU, over every run (100) requested. It is important to note that each
run will have a different randomly generated demand. Due to the randomised demand, the transaction summary for the same
SKU will differ over successive runs. The spread of data captures the statistically probable distribution of demand the
SKU can expect. However the more runs (thousands, tens of thousands), the more useful the result.

.. parsed-literal::

    {'standard_deviation_backlog': 250.43961347997646, 'variance_quantity_sold': 4045303.0763888955,
    'total_shortage_units': 672.0, 'average_closing_stock': 3028.416748046875, 'maximum_opening_stock': 6279.0,
    'minimum_closing_stock': 0.0, 'maximum_shortage_units': 672.0, 'variance_backlog': 62720.0,
    'average_quantity_sold': 3091.583251953125, 'minimum_backlog': 0.0, 'maximum_backlog': 672.0,
    'minimum_opening_stock': 0.0, 'standard_deviation_opening_stock': 2082.4554600412375, 'sku_id': 'KR202-230',
    'standard_deviation_revenue': 2011.2938811593137, 'maximum_quantity_sold': 6278.0,
    'average_opening_stock': 2994.916748046875, 'minimum_quantity_sold': 537.0, 'maximum_closing_stock': 6279.0,
    'stockout_percentage': 0.0833333358168602, 'variance_opening_stock': 4336620.7430555625,
    'variance_shortage_units': 34496.0, 'standard_deviation_closing_stock': 2096.713160255569,
    'average_backlog': 112.0, 'variance_closing_stock': 4396206.0763888955,
    'standard_deviation_shortage_cost': 185.7309882599024, 'minimum_shortage_units': 0.0, 'index': '22'}

This analysis completed in:

     +-------+----------------------+
     | system| time (seconds)       |
     +=======+======================+
     |  PC   | 372.97969007492065   |
     +-------+----------------------+
     |  Mac  | 506.49058294296265   |
     +-------+----------------------+

The `summarize_window` returns max, min, averages and standard deviations for key values from the transaction summary.

The last method summarizes the runs into one transaction summary for each sku. Similar in content to the previous
summary however this summary aggregates the simulation runs.

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> from supplychainpy import simulate
    >>>
    >>> orders_analysis = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>>
    >>> sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, runs=100, period_length=12)
    >>>
    >>> sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)
    >>>
    >>> sim_frame= simulate.summarise_frame(sim_window)
    >>>
    >>> for transaction_summary in sim_frame:
    >>>		print(transaction_summary)


Below is 1 of 32 result for 32 skus ran 100 times.

.. parsed-literal::

    {'standard_deviation_quantity_sold': '2228', 'average_backlog': '0', 'standard_deviation_closing_stock': '2228',
    'maximum_quantity_sold': 7901.0, 'sku_id': 'KR202-209', 'minimum_quantity_sold': 407.0, 'minimum_backlog': 0.0,
    'average_closing_stock': '3592', 'average_shortage_units': '0', 'variance_opening_stock': '2287',
    'minimum_opening_stock': 407, 'maximum_opening_stock': 7901, 'minimum_closing_stock': 407, 'service_level': '100.00',
    'maximum_closing_stock': 7901, 'average_quantity_sold': '3592', 'standard_deviation_backlog': '0',
    'maximum_backlog': 0.0}

The analysis completed in:

     +-------+----------------------+
     | system| time (seconds)       |
     +=======+======================+
     |  PC   | 388.324289560318     |
     +-------+----------------------+
     |  Mac  | 562.0152740478516    |
     +-------+----------------------+

An optimisation option exists, if after running the Monte Carlo analysis, the behaviour in
the transaction summary is not favourable. If most SKUs are not achieving their desired service level or have large
quantities of backlog etc., then you can use:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> from supplychainpy import simulate
    >>>
    >>> orders_analysis = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>>
    >>> sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, runs=100, period_length=12)
    >>>
    >>> sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)
    >>>
    >>> sim_frame= simulate.summarise_frame(sim_window)
    >>>
    >>> optimised_orders = simulate.optimise_service_level(service_level=95.0, frame_summary=sim_frame,
    >>>                                            orders_analysis=orders_analysis.orders, runs=100, percentage_increase=1.30)


The `optimise_service_level` methods take a value for the desired service level, the transaction summary of the
Monte Carlo simulation and the original orders analysis. The service level achieved in the Monte Carlo analysis is
reviewed and compared with the desired service level. If below a threshold, then the safety stock is increased and the
whole Monte Carlo simulation is run again. The supplied variable percentage_increase specifies the growth in safety stock.

This optimisation step will take as long, if not longer, than the initial Monte Carlo simulation because the optimisation
step runs the simulation again to simulate transactions based on the new safety stock values. Please take this into
consideration and adjust your expectation for this optimisation step.
This feature is in development as is the whole library but this feature will change in the next release.

For further details on the implementation, please view the `deep-dive blog posts <http://www.supplychainpy.org/blog/>`_
for each release.

