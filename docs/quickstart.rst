Quick Guide
===========

.. warning::
	The library is currently under development and in planning stages. The library should not be used in
	production at this time.


.. note::

    All profiling has been carried out on the following systems:

    +------------+------------------------------------+------------------+----------------+
    | system     |           CPU                      | Ram              |  OS            |
    +============+====================================+==================+================+
    |   PC       | Xeon 1650v3 (15M Cache, 3.50 GHz)  | 32gb ddr4 2133   | linux (xubuntu)|
    +------------+------------------------------------+------------------+----------------+
    | Macbook Air|            i7-4650U                |   8gb ddr3 1600  | OS X (yosemite)|
    +------------+------------------------------------+------------------+----------------+

    Timings are provided as simple benchmarks and will vary based on system and current load.
    The computations here are mainly cpu bound, io may be a factor when reading from file (csv txt).

Overview
--------

Supplychainpy is a Python library for supply chain analysis, modeling and simulation. Using supplychainpy
with popular data analysis libraries and tools such as Xlwings or Data Nitro (for Excel spreadsheet applications),
Pandas, NumPy, Matplotlib, Ipython and Jupyter makes for a powerful supply chain data analysis toolchain.

While the supplychainpy library can be used in any way you deem fit, the library was created to assist a workflow that
is reliant on Excel, Excel formulas and VBA. Below we go through the use cases and implementations specific to the
domain (supply chain, operations and manufacturing).

This quick guide is skewed towards analysts with the requisite domain knowledge, who predominantly use Excel. Some
knowledge of Python or programming is assumed, although those new to data analysis or using python will likely be able to
follow with assistance from other material.

The following guide assumes that the supplychainpy library has already been installed. If not please use the
instructions for :ref:`Installation`.


Inventory Analysis
------------------

A quick example of a typical inventory analysis takes several formulas, manual processes or pivot tables and in
some cases vba to achieve. Using the supplychainpy library can reduce the time and effort taken for the same analysis.
In the example below supplying a `dict` of "Orders" data-points can generate a summary.

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


Currently the `lead_time` and the `yearly_demand` parameters, must be in the same units (the user must make the correct conversion).
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

A file named `data.csv`, supplied with this distribution (release 0.0.2 onwards) can be used to generate the
same analysis in `dict` based example. The example below generates the result for 32 stock keeping units (sku).

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> print (abc.abcxyz_summary)

.. parsed-literal::


    [{'AX': 0}, {'AY': 14}, {'AZ': 7}, {'BX': 0}, {'BY': 3}, {'BZ': 2}, {'CX': 0}, {'CY': 3}, {'CZ': 3}]

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
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> for sku in abc.orders:
    >>>     print('Sku: {} Economic Order Quantity: {:.0f} Sku Revenue: {:.0f} ABCXYZ Classification: {}'.format(sku.sku_id,
    >>>                                                 sku.economic_order_qty, sku.revenue, sku.abcxyz_classification))

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

This analysis completed in:

	 +-------+----------------------+
	 | system| time (seconds)       |
	 +=======+======================+
	 |  PC   | 0.0178067684173584   |
	 +-------+----------------------+
	 |  Mac  | 0.024185895919799805 |
	 +-------+----------------------+

The best way to retrieve a full summary is by doing the following:

.. code:: python

    >>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
    >>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
    >>>                                        reorder_cost=Decimal(5000), file_type="csv")
    >>> for sku in abc.orders:
	>>>		print(sku.orders_summary())

.. parsed-literal::

	{'reorder_quantity': '380', 'economic_order_quantity': '1311', 'sku': 'KR202-209', 'standard_deviation': '976',
	'ABC_XYZ_Classification': 'CZ', 'demand_variability': '0.675', 'safety_stock': '1767', 'average_order': '1446',
	'revenue': '6942800.00', 'economic_order_variable_cost': '186365.16', 'reorder_level': '3812'}
	{'reorder_quantity': '410', 'economic_order_quantity': '1405', 'sku': 'KR202-210', 'standard_deviation': '960',
	'ABC_XYZ_Classification': 'CY', 'demand_variability': '0.560', 'safety_stock': '1700', 'average_order': '1700',
	'revenue': '7900000.00', 'economic_order_variable_cost': '196720.63', 'reorder_level': '4100'}
	{'reorder_quantity': '350', 'economic_order_quantity': '1224', 'sku': 'KR202-211', 'standard_deviation': '790',
	'ABC_XYZ_Classification': 'CZ', 'demand_variability': '0.610', 'safety_stock': '2000', 'average_order': '1300',
	'revenue': '6900000.00', 'economic_order_variable_cost': '188736.92', 'reorder_level': '4600'}
	{'reorder_quantity': '390', 'economic_order_quantity': '1317', 'sku': 'KR202-212', 'standard_deviation': '1000',
	'ABC_XYZ_Classification': 'BY', 'demand_variability': '0.560', 'safety_stock': '2200', 'average_order': '1800',
	'revenue': '10000000.00', 'economic_order_variable_cost': '221742.57', 'reorder_level': '5300'}
	{'reorder_quantity': '290', 'economic_order_quantity': '981', 'sku': 'KR202-213', 'standard_deviation': '610',
	'ABC_XYZ_Classification': 'CY', 'demand_variability': '0.550', 'safety_stock': '780', 'average_order': '1100',
	'revenue': '6700000.00', 'economic_order_variable_cost': '179194.80', 'reorder_level': '1900'}
	{'reorder_quantity': '330', 'economic_order_quantity': '1170', 'sku': 'KR202-214', 'standard_deviation': '750',
	'ABC_XYZ_Classification': 'BY', 'demand_variability': '0.500', 'safety_stock': '1300', 'average_order': '1500',
	'revenue': '10000000.00', 'economic_order_variable_cost': '230255.37', 'reorder_level': '3400'}
	{'reorder_quantity': '290', 'economic_order_quantity': '1030', 'sku': 'KR202-215', 'standard_deviation': '730',
	'ABC_XYZ_Classification': 'CY', 'demand_variability': '0.560', 'safety_stock': '930', 'average_order': '1300',
	'revenue': '9500000.00', 'economic_order_variable_cost': '217357.95', 'reorder_level': '2200'}
	{'reorder_quantity': '310', 'economic_order_quantity': '1054', 'sku': 'KR202-216', 'standard_deviation': '870',
	'ABC_XYZ_Classification': 'BY', 'demand_variability': '0.580', 'safety_stock': '1900', 'average_order': '1500',
	'revenue': '11000000.00', 'economic_order_variable_cost': '237449.51', 'reorder_level': '4500'}
	{'reorder_quantity': '320', 'economic_order_quantity': '1083', 'sku': 'KR202-217', 'standard_deviation': '850',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.500', 'safety_stock': '1900', 'average_order': '1700',
	'revenue': '13000000.00', 'economic_order_variable_cost': '259467.97', 'reorder_level': '4800'}
	{'reorder_quantity': '250', 'economic_order_quantity': '862', 'sku': 'KR202-218', 'standard_deviation': '750',
	'ABC_XYZ_Classification': 'CZ', 'demand_variability': '0.680', 'safety_stock': '1300', 'average_order': '1100',
	'revenue': '9300000.00', 'economic_order_variable_cost': '218563.26', 'reorder_level': '2800'}
	{'reorder_quantity': '260', 'economic_order_quantity': '894', 'sku': 'KR202-219', 'standard_deviation': '840',
	'ABC_XYZ_Classification': 'BZ', 'demand_variability': '0.650', 'safety_stock': '1900', 'average_order': '1300',
	'revenue': '11000000.00', 'economic_order_variable_cost': '239468.13', 'reorder_level': '4100'}
	{'reorder_quantity': '280', 'economic_order_quantity': '967', 'sku': 'KR202-220', 'standard_deviation': '710',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.440', 'safety_stock': '1500', 'average_order': '1600',
	'revenue': '15000000.00', 'economic_order_variable_cost': '272793.81', 'reorder_level': '4200'}
	{'reorder_quantity': '270', 'economic_order_quantity': '937', 'sku': 'KR202-221', 'standard_deviation': '740',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.490', 'safety_stock': '1300', 'average_order': '1500',
	'revenue': '15000000.00', 'economic_order_variable_cost': '277746.69', 'reorder_level': '3400'}
	{'reorder_quantity': '240', 'economic_order_quantity': '848', 'sku': 'KR202-222', 'standard_deviation': '960',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.740', 'safety_stock': '1700', 'average_order': '1300',
	'revenue': '13000000.00', 'economic_order_variable_cost': '263233.01', 'reorder_level': '3500'}
	{'reorder_quantity': '280', 'economic_order_quantity': '932', 'sku': 'KR202-223', 'standard_deviation': '910',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.510', 'safety_stock': '1200', 'average_order': '1800',
	'revenue': '19000000.00', 'economic_order_variable_cost': '302568.86', 'reorder_level': '3000'}
	{'reorder_quantity': '250', 'economic_order_quantity': '863', 'sku': 'KR202-224', 'standard_deviation': '770',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.510', 'safety_stock': '1400', 'average_order': '1500',
	'revenue': '17000000.00', 'economic_order_variable_cost': '292679.11', 'reorder_level': '3500'}
	{'reorder_quantity': '280', 'economic_order_quantity': '960', 'sku': 'KR202-225', 'standard_deviation': '790',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.420', 'safety_stock': '2400', 'average_order': '1900',
	'revenue': '23000000.00', 'economic_order_variable_cost': '338919.52', 'reorder_level': '7000'}
	{'reorder_quantity': '200', 'economic_order_quantity': '715', 'sku': 'KR202-226', 'standard_deviation': '750',
	'ABC_XYZ_Classification': 'BZ', 'demand_variability': '0.680', 'safety_stock': '1600', 'average_order': '1100',
	'revenue': '13000000.00', 'economic_order_variable_cost': '262606.41', 'reorder_level': '3500'}
	{'reorder_quantity': '250', 'economic_order_quantity': '861', 'sku': 'KR202-227', 'standard_deviation': '1000',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.590', 'safety_stock': '2200', 'average_order': '1700',
	'revenue': '21000000.00', 'economic_order_variable_cost': '328549.13', 'reorder_level': '5100'}
	{'reorder_quantity': '230', 'economic_order_quantity': '794', 'sku': 'KR202-228', 'standard_deviation': '910',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.610', 'safety_stock': '1700', 'average_order': '1500',
	'revenue': '20000000.00', 'economic_order_variable_cost': '314247.52', 'reorder_level': '3800'}
	{'reorder_quantity': '210', 'economic_order_quantity': '722', 'sku': 'KR202-229', 'standard_deviation': '760',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.580', 'safety_stock': '1400', 'average_order': '1300',
	'revenue': '17000000.00', 'economic_order_variable_cost': '296235.01', 'reorder_level': '3200'}
	{'reorder_quantity': '240', 'economic_order_quantity': '838', 'sku': 'KR202-230', 'standard_deviation': '710',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.420', 'safety_stock': '1300', 'average_order': '1700',
	'revenue': '24000000.00', 'economic_order_variable_cost': '355615.36', 'reorder_level': '3700'}
	{'reorder_quantity': '210', 'economic_order_quantity': '771', 'sku': 'KR202-231', 'standard_deviation': '1000',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.710', 'safety_stock': '2600', 'average_order': '1400',
	'revenue': '21000000.00', 'economic_order_variable_cost': '337895.30', 'reorder_level': '5400'}
	{'reorder_quantity': '230', 'economic_order_quantity': '815', 'sku': 'KR202-232', 'standard_deviation': '760',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.450', 'safety_stock': '1400', 'average_order': '1700',
	'revenue': '25000000.00', 'economic_order_variable_cost': '368695.10', 'reorder_level': '3800'}
	{'reorder_quantity': '190', 'economic_order_quantity': '654', 'sku': 'KR202-233', 'standard_deviation': '960',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.800', 'safety_stock': '2400', 'average_order': '1200',
	'revenue': '18000000.00', 'economic_order_variable_cost': '305508.97', 'reorder_level': '4800'}
	{'reorder_quantity': '180', 'economic_order_quantity': '631', 'sku': 'KR202-234', 'standard_deviation': '520',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.470', 'safety_stock': '940', 'average_order': '1100', '
	revenue': '18000000.00', 'economic_order_variable_cost': '303802.21', 'reorder_level': '2400'}
	{'reorder_quantity': '230', 'economic_order_quantity': '810', 'sku': 'KR202-235', 'standard_deviation': '710',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.390', 'safety_stock': '1500', 'average_order': '1800',
	'revenue': '31000000.00', 'economic_order_variable_cost': '401004.30', 'reorder_level': '4600'}
	{'reorder_quantity': '190', 'economic_order_quantity': '622', 'sku': 'KR202-236', 'standard_deviation': '910',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.700', 'safety_stock': '2000', 'average_order': '1300',
	'revenue': '22000000.00', 'economic_order_variable_cost': '316943.99', 'reorder_level': '4200'}
	{'reorder_quantity': '200', 'economic_order_quantity': '671', 'sku': 'KR202-237', 'standard_deviation': '1000',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.670', 'safety_stock': '1800', 'average_order': '1500',
	'revenue': '27000000.00', 'economic_order_variable_cost': '351630.69', 'reorder_level': '3900'}
	{'reorder_quantity': '200', 'economic_order_quantity': '685', 'sku': 'KR202-238', 'standard_deviation': '600',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.400', 'safety_stock': '1300', 'average_order': '1500',
	'revenue': '27000000.00', 'economic_order_variable_cost': '368603.50', 'reorder_level': '3900'}
	{'reorder_quantity': '210', 'economic_order_quantity': '713', 'sku': 'KR202-239', 'standard_deviation': '800',
	'ABC_XYZ_Classification': 'AY', 'demand_variability': '0.470', 'safety_stock': '1400', 'average_order': '1700',
	'revenue': '31000000.00', 'economic_order_variable_cost': '393826.78', 'reorder_level': '3800'}
	{'reorder_quantity': '190', 'economic_order_quantity': '680', 'sku': 'KR202-240', 'standard_deviation': '960',
	'ABC_XYZ_Classification': 'AZ', 'demand_variability': '0.690', 'safety_stock': '2000', 'average_order': '1400',
	'revenue': '27000000.00', 'economic_order_variable_cost': '384904.27', 'reorder_level': '4400'}


This analysis completed in:

	 +-------+----------------------+
	 | system| time (seconds)       |
	 +=======+======================+
	 |  PC   | 0.009218931198120117 |
	 +-------+----------------------+
	 |  Mac  | 0.02485513687133789  |
	 +-------+----------------------+

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
does not capture. The monte carlo simulation is useful when complicated interactions and affects are not adequately
captured by an analytical model. A simulation is useful for giving a dynamic view of a complex operation.
The simulation replicates some of the complexity of the system over time.

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

The transactions over the 12 periods are summarised for each sku and for every run (100) requested. It is important to note
that each run will have a different randomly generated demand. Due to the randomised demand, the transaction summary for the same sku, will differ over
successive runs. The spread of data captures the statistically probable distribution of demand the sku can expect.

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
	 ...

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

An optimisation option exists, if after running the monte carlo analysis, the behaviour in
the transaction summary is not favourable. If most skus are not achieving their desired service level, or have large
quantities of backlog etc, then you can use:

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


The `optimise_service_level` methods takes a value for the desired service level, the transaction summary of the
monte carlo simulation and the original orders analysis. The service level achieved in the monte carlo analysis is
reviewed and compared with the desired service level. If below a threshold, then the safety stock is increased and the
whole monte carlo simulation is run again. The increase in safety stock is specified by the supplied variable
percentage_increase.

This optimisation step will take as long, if not longer, than the initial monte carlo simulation because the optimisation
step run the simulation again to simulate transactions based on the new safety stock values. Please take this into
consideration and adjust your expectation for this optimisation step.
This feature is in development as is the whole library but this feature will change in the next release.




