.. _inventory:

Inventory Modeling and Analysis Made Easy with Supplychainpy
============================================================

The following is taken from the jupyter notebook title '0.0.4-Inventory-Modeling-v1' found `here <https://github.com/KevinFasusi/supplychainpy_notebooks>`_ .
For a more interactive experience please retrieve this notebook and run with jupyter.

This workbook assumes some familiarity and proficiency in programming
with Python. Understanding list comprehensions, conditional logic, loops
and functions are a basic prequisite for continuing with this workbook.

Typically, inventory analysis using Excel requires several formulas,
manual processes, possibly some pivot tables and in some cases VBA to
achieve. Using the supplychainpy library can reduce the time taken and
effort made for the same analysis.

.. code:: python

    from supplychainpy.model_inventory import analyse
    from decimal import Decimal
    from supplychainpy.sample_data.config import ABS_FILE_PATH

The first two imports are manditory, the second import is for using the
sample data in the ``supplychainpy`` library. When working with a
different file, supply the file path to the ``file_path`` parameter. The
data supplied for analysis can be from a ``csv`` or a database ETL
process.

The sample data is a ``csv`` formatted file:

.. code:: python

    with open(ABS_FILE_PATH['COMPLETE_CSV_SM'],'r') as raw_data:
        for line in raw_data:
            print(line)


.. parsed-literal::

    Sku,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,unit cost,lead-time,retail_price,quantity_on_hand,backlog
    
    KR202-209,1509,1855,2665,1841,1231,2598,1988,1988,2927,2707,731,2598,1001,2,5000,1003,10
    
    KR202-210,1006,206,2588,670,2768,2809,1475,1537,919,2525,440,2691,394,2,1300,3224,10
    
    KR202-211,1840,2284,850,983,2737,1264,2002,1980,235,1489,218,525,434,4,1200,390,10
    
    KR202-212,104,2262,350,528,2570,1216,1101,2755,2856,2381,1867,2743,474,3,10,390,10
    
    KR202-213,489,954,1112,199,919,330,561,2372,921,1587,1532,1512,514,1,2000,2095,10
    
    KR202-214,2416,2010,2527,1409,1059,890,2837,276,987,2228,1095,1396,554,2,1800,55,10
    
    KR202-215,403,1737,753,1982,2775,380,1561,1230,1262,2249,824,743,594,1,2500,4308,10
    
    KR202-216,2908,929,684,2618,1477,1508,765,43,2550,2157,937,1201,634,3,3033,34,10
    
    KR202-217,2799,2197,1647,2263,224,2987,2366,588,1140,869,1707,1180,674,3,5433,390,10
    
    KR202-218,1333,402,804,318,1408,830,1028,534,1871,2730,2022,94,714,2,3034,3535,10
    
    KR202-219,813,969,745,1001,2732,1987,717,599,2722,171,639,2108,754,3,5000,334,10
    
    KR202-220,1481,905,1067,2513,861,1670,650,2630,1245,997,1936,2780,794,3,7500,3434,10
    
    KR202-221,771,2941,1360,2714,1801,1744,1428,1660,436,578,1956,1101,834,2,4938,4433,10
    
    KR202-222,2349,4,345,524,340,2698,2137,1164,498,1583,1241,2965,874,2,4922,3435,10
    
    KR202-223,2045,2055,552,81,2780,176,2316,1475,2566,1678,1553,2745,914,1,4894,34533,10
    
    KR202-224,2482,1887,1911,1446,2939,1241,1281,692,119,627,1941,1383,954,2,2942,33,10
    
    KR202-225,2744,2770,2697,1726,1776,2264,332,2420,2722,1161,1986,2587,994,6,8999,2000,10
    
    KR202-226,2509,914,903,877,1859,2263,383,593,236,189,920,1686,1034,3,4342,4344,10
    
    KR202-227,368,2502,2955,2994,1270,2884,2208,699,854,877,2320,160,1074,3,4920,489,10
    
    KR202-228,1468,1109,2464,2799,948,589,2858,1140,501,2691,93,1060,1114,2,15000,9439,10
    
    KR202-229,2114,198,1479,1249,1475,744,407,2280,226,2285,796,1948,1154,2,13000,8939,10
    
    KR202-230,1023,1150,1672,2026,1590,441,2484,2300,2928,1082,2064,2412,1194,2,10000,349,10
    
    KR202-231,482,546,299,2304,2953,1029,1863,2809,454,927,2488,2341,1234,4,9999,3434,10
    
    KR202-232,614,2138,962,2017,2398,2963,2189,1804,414,2016,1350,2464,1274,2,7500,234,10
    
    KR202-233,2395,2521,2157,728,1028,43,138,826,570,2825,181,787,1314,4,6000,349,10
    
    KR202-234,1336,1478,865,533,1562,422,2287,1302,1230,1059,1153,399,1354,2,20000,324,10
    
    KR202-235,2565,2762,2721,1431,845,2163,2413,2227,1753,740,1139,2300,1394,3,59500,850,10
    
    KR202-236,1912,1726,1569,316,71,2082,108,174,1974,609,2896,566,1434,3,2300,4930,10
    
    KR202-237,2153,1112,16,130,590,2619,2576,2390,2567,1531,842,242,1474,2,4500,9483,10
    
    KR202-238,1417,2044,1981,1936,2377,780,1544,1521,51,1056,1876,1356,1514,3,8000,839,10
    
    KR202-239,2717,2186,2300,677,2157,2328,1917,2519,561,281,1162,1146,1554,2,39000,433,10
    
    KR202-240,1015,741,2754,2925,2302,695,2869,440,406,1083,2334,1015,1594,3,3943,390,10
    
    KR202-241,3050,1507,3637,1112,1963,1675,898,1986,2262,3895,1229,2904,769,5,8007,2125,10
    
    KR202-242,1875,2368,830,823,868,1409,1845,3095,3247,1894,2558,3048,1819,1,13225,1253,10
    
    KR202-243,1717,593,3006,2935,3139,2753,3247,3845,1720,3413,3399,2799,1120,3,14682,1128,10
    
    KR202-244,2383,2046,2487,3827,1674,3118,2849,2233,3888,2566,2216,3817,1067,5,11997,1191,10
    
    KR202-245,1115,2694,3038,3366,1058,2724,2863,1930,1787,838,3087,1565,1623,2,12876,611,10
    
    KR202-246,3108,1197,2472,1264,3179,3638,1268,1581,3456,1630,1788,2288,608,2,6548,2192,10
    
    KR202-247,3439,1854,652,1827,1645,2257,2733,1337,2034,2106,877,2409,1578,2,10463,1017,10


It is probable that getting the data to this format will require
'extracting' from a database and 'transforming' data before 'loading'
into the ``analyse`` function. This can be achieved with an orm like
slqalchemy or using the driver for the database in question.
Supplychainpy works with Pandas so performing the transformations using
Pandas may be an idea. The ``DataFrame`` or file passed as an argument
must be identical to the format above (future versions of supplychainpy
will be more lenient and attempt to identify if a minimum requirement
has been met).

The ETL process is not covered in this workbook but on the 'roadmap' for
``supplychainpy`` is the automation of this process.

So now that we have the data in the correct format we can proceed with
the anlysis.

.. code:: python

    #%%timeit
    analysed_inventory_profile= analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                                                 z_value=Decimal(1.28),
                                                                 reorder_cost=Decimal(400),
                                                                 file_type='csv')


The variable ``analysed_inventory_profile`` now contains a collection
(list) of ``UncertainDemand`` objects (one per SKU). Each object
contains the analysis for each SKU. The analysis include the following:

-  safety stock
-  total\_orders
-  standard\_deviation
-  quantity\_on\_hand': '1003
-  economic\_order\_variable\_cost
-  sku
-  economic\_order\_quantity
-  unit\_cost
-  demand\_variability
-  average\_orders
-  excess\_stock
-  currency
-  ABC\_XYZ\_Classification
-  shortages
-  reorder\_level
-  revenue
-  reorder\_quantity
-  safety\_stock
-  orders

The listed summary items can be retrieved by calling the method
``orders_summary()`` on each object. The quickest way to do this is with
a list comprehension.

.. code:: python

    analysis_summary = [demand.orders_summary() for demand in analysed_inventory_profile]

For the intrepid reader who did not heed the warning about the
prerequisites and is now scratching their head wondering "what manner of
black magic is this," here is a quick overview on list comprehensions.
In short, the above code is similar to the code below:

.. code:: python

    analysis_summary =[]
    for demand in analysed_inventory_profile:
        analysis_summary.append(demand.orders_summary())

The former is much more readable and in truth quite addictive (hence the
warning, the love for list comprehensions runs deep).

Exploring the results
---------------------

To make sense of the results we can filter our analysis using standard
python scripting techniques. For example to retrieve the whole
``summary`` for the SKU ``KR202-209`` we can do something like this:

.. code:: python

    %%timeit
    sku_summary = [demand.orders_summary() for demand in analysed_inventory_profile if demand.orders_summary().get('sku')== 'KR202-209']
    #print(sku_summary)


.. parsed-literal::

    1000 loops, best of 3: 885 µs per loop


The inventory classification ABC XYZ denotes the SKUs contribution to
revenue and demand volatility. ``AX`` SKUs typically exhibit steady
demand and contribute 80% of the revenue value for the period being
analysed. Further explanation on ``ABC XYZ`` analysis can be found here.

As a more traditional way of grouping SKUs by behaviour, it is also
likely to be used for generating inventory policies and for further
exploration of the inventory profile. To retrive all the summaries for a
particular classification, we could do something like this:

.. code:: python

    ay_classification_summary = [demand.orders_summary() for demand in analysed_inventory_profile if demand.orders_summary().get('ABC_XYZ_Classification')== 'AY']
    print(ay_classification_summary)


.. parsed-literal::

    [{'total_orders': '25185', 'standard_deviation': '721', 'quantity_on_hand': '2000', 'economic_order_variable_cost': '15826.20', 'sku': 'KR202-225', 'economic_order_quantity': '45', 'unit_cost': '994', 'demand_variability': '0.344', 'average_orders': '2098.75', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '10542', 'reorder_level': '7402', 'revenue': '226639815', 'reorder_quantity': '13', 'safety_stock': '2261', 'orders': {'demand': ('2744', '2770', '2697', '1726', '1776', '2264', '332', '2420', '2722', '1161', '1986', '2587')}}, {'total_orders': '15201', 'standard_deviation': '752', 'quantity_on_hand': '8939', 'economic_order_variable_cost': '13248.03', 'sku': 'KR202-229', 'economic_order_quantity': '32', 'unit_cost': '1154', 'demand_variability': '0.594', 'average_orders': '1266.75', 'excess_stock': '3994', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '0', 'reorder_level': '3153', 'revenue': '197613000', 'reorder_quantity': '9', 'safety_stock': '1362', 'orders': {'demand': ('2114', '198', '1479', '1249', '1475', '744', '407', '2280', '226', '2285', '796', '1948')}}, {'total_orders': '21172', 'standard_deviation': '702', 'quantity_on_hand': '349', 'economic_order_variable_cost': '15903.60', 'sku': 'KR202-230', 'economic_order_quantity': '37', 'unit_cost': '1194', 'demand_variability': '0.398', 'average_orders': '1764.3333', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '5913', 'reorder_level': '3767', 'revenue': '211720000', 'reorder_quantity': '11', 'safety_stock': '1271', 'orders': {'demand': ('1023', '1150', '1672', '2026', '1590', '441', '2484', '2300', '2928', '1082', '2064', '2412')}}, {'total_orders': '21329', 'standard_deviation': '749', 'quantity_on_hand': '234', 'economic_order_variable_cost': '16488.55', 'sku': 'KR202-232', 'economic_order_quantity': '36', 'unit_cost': '1274', 'demand_variability': '0.422', 'average_orders': '1777.4167', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '6150', 'reorder_level': '3870', 'revenue': '159967500', 'reorder_quantity': '11', 'safety_stock': '1356', 'orders': {'demand': ('614', '2138', '962', '2017', '2398', '2963', '2189', '1804', '414', '2016', '1350', '2464')}}, {'total_orders': '13626', 'standard_deviation': '516', 'quantity_on_hand': '324', 'economic_order_variable_cost': '13586.45', 'sku': 'KR202-234', 'economic_order_quantity': '28', 'unit_cost': '1354', 'demand_variability': '0.454', 'average_orders': '1135.5', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '3822', 'reorder_level': '2540', 'revenue': '272520000', 'reorder_quantity': '8', 'safety_stock': '934', 'orders': {'demand': ('1336', '1478', '865', '533', '1562', '422', '2287', '1302', '1230', '1059', '1153', '399')}}, {'total_orders': '23059', 'standard_deviation': '691', 'quantity_on_hand': '850', 'economic_order_variable_cost': '17933.46', 'sku': 'KR202-235', 'economic_order_quantity': '36', 'unit_cost': '1394', 'demand_variability': '0.360', 'average_orders': '1921.5833', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '7339', 'reorder_level': '4861', 'revenue': '1372010500', 'reorder_quantity': '11', 'safety_stock': '1532', 'orders': {'demand': ('2565', '2762', '2721', '1431', '845', '2163', '2413', '2227', '1753', '740', '1139', '2300')}}, {'total_orders': '19951', 'standard_deviation': '811', 'quantity_on_hand': '433', 'economic_order_variable_cost': '17612.47', 'sku': 'KR202-239', 'economic_order_quantity': '32', 'unit_cost': '1554', 'demand_variability': '0.488', 'average_orders': '1662.5833', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '5737', 'reorder_level': '3819', 'revenue': '778089000', 'reorder_quantity': '9', 'safety_stock': '1468', 'orders': {'demand': ('2717', '2186', '2300', '677', '2157', '2328', '1917', '2519', '561', '281', '1162', '1146')}}, {'total_orders': '26118', 'standard_deviation': '950', 'quantity_on_hand': '2125', 'economic_order_variable_cost': '14175.73', 'sku': 'KR202-241', 'economic_order_quantity': '52', 'unit_cost': '769', 'demand_variability': '0.437', 'average_orders': '2176.5', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '10328', 'reorder_level': '7586', 'revenue': '209126826', 'reorder_quantity': '15', 'safety_stock': '2719', 'orders': {'demand': ('3050', '1507', '3637', '1112', '1963', '1675', '898', '1986', '2262', '3895', '1229', '2904')}}, {'total_orders': '23860', 'standard_deviation': '853', 'quantity_on_hand': '1253', 'economic_order_variable_cost': '20838.38', 'sku': 'KR202-242', 'economic_order_quantity': '32', 'unit_cost': '1819', 'demand_variability': '0.429', 'average_orders': '1988.3333', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '0', 'reorder_level': '3080', 'revenue': '315548500', 'reorder_quantity': '9', 'safety_stock': '1092', 'orders': {'demand': ('1875', '2368', '830', '823', '868', '1409', '1845', '3095', '3247', '1894', '2558', '3048')}}, {'total_orders': '32566', 'standard_deviation': '882', 'quantity_on_hand': '1128', 'economic_order_variable_cost': '19103.09', 'sku': 'KR202-243', 'economic_order_quantity': '48', 'unit_cost': '1120', 'demand_variability': '0.325', 'average_orders': '2713.8333', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '10227', 'reorder_level': '6655', 'revenue': '478134012', 'reorder_quantity': '14', 'safety_stock': '1954', 'orders': {'demand': ('1717', '593', '3006', '2935', '3139', '2753', '3247', '3845', '1720', '3413', '3399', '2799')}}, {'total_orders': '33104', 'standard_deviation': '718', 'quantity_on_hand': '1191', 'economic_order_variable_cost': '18799.00', 'sku': 'KR202-244', 'economic_order_quantity': '50', 'unit_cost': '1067', 'demand_variability': '0.260', 'average_orders': '2758.6667', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '13200', 'reorder_level': '8223', 'revenue': '397148688', 'reorder_quantity': '14', 'safety_stock': '2054', 'orders': {'demand': ('2383', '2046', '2487', '3827', '1674', '3118', '2849', '2233', '3888', '2566', '2216', '3817')}}, {'total_orders': '26065', 'standard_deviation': '855', 'quantity_on_hand': '611', 'economic_order_variable_cost': '20573.14', 'sku': 'KR202-245', 'economic_order_quantity': '36', 'unit_cost': '1623', 'demand_variability': '0.394', 'average_orders': '2172.0833', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '7081', 'reorder_level': '4620', 'revenue': '335612940', 'reorder_quantity': '10', 'safety_stock': '1548', 'orders': {'demand': ('1115', '2694', '3038', '3366', '1058', '2724', '2863', '1930', '1787', '838', '3087', '1565')}}, {'total_orders': '26869', 'standard_deviation': '872', 'quantity_on_hand': '2192', 'economic_order_variable_cost': '12784.68', 'sku': 'KR202-246', 'economic_order_quantity': '59', 'unit_cost': '608', 'demand_variability': '0.389', 'average_orders': '2239.0833', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '0', 'reorder_level': '4745', 'revenue': '175938212', 'reorder_quantity': '17', 'safety_stock': '1578', 'orders': {'demand': ('3108', '1197', '2472', '1264', '3179', '3638', '1268', '1581', '3456', '1630', '1788', '2288')}}, {'total_orders': '23170', 'standard_deviation': '735', 'quantity_on_hand': '1017', 'economic_order_variable_cost': '19126.21', 'sku': 'KR202-247', 'economic_order_quantity': '34', 'unit_cost': '1578', 'demand_variability': '0.381', 'average_orders': '1930.8333', 'excess_stock': '0', 'currency': 'UNKNOWN', 'ABC_XYZ_Classification': 'AY', 'shortages': '5776', 'reorder_level': '4062', 'revenue': '242427710', 'reorder_quantity': '10', 'safety_stock': '1331', 'orders': {'demand': ('3439', '1854', '652', '1827', '1645', '2257', '2733', '1337', '2034', '2106', '877', '2409')}}]


Using a built-in feature of the library provides a quicker way to filter
the results. For example a quciker way to filter for SKU ``KR202-209``,
is through the use of ``Inventory`` class in the ``summarise`` module.

.. code:: python

    from supplychainpy.inventory.summarise import Inventory
    filtered_summary = Inventory(analysed_inventory_profile)

.. code:: python

    %%timeit
    sku_summary = [summary for summary in filtered_summary.describe_sku('KR202-209')]
    #print(sku_summary)


.. parsed-literal::

    10000 loops, best of 3: 190 µs per loop


Using the import Inventory specifically built to filter the analysis is
faster and syntactically cleaner for eaier to read and understand code.
The ``Inventory`` summary class also provides a more detailed summary of
the SKU with additional KPIs and metric in context of the whole
inventory profile. The summary ranks and performs some comparative
analysis for more insight.

The descriptive summary includes:

-  shortage\_rank
-  min\_orders
-  excess\_units
-  revenue\_rank
-  excess\_rank
-  average\_orders
-  gross\_profit\_margin
-  markup\_percentage
-  max\_order
-  shortage\_cost
-  quantity\_on\_hand
-  inventory\_turns
-  sku\_id
-  retail\_price
-  revenue\_rank
-  shortage\_units
-  unit\_cost
-  classification
-  safety\_stock\_cost
-  safety\_stock\_units
-  safety\_stock\_rank
-  percentage\_contribution\_revenue
-  gross\_profit\_margin
-  shortage\_rank
-  inventory\_traffic\_light
-  unit\_cost\_rank
-  excess\_cost
-  excess\_units
-  markup\_percentage
-  revenue

This is a pretty comprehensive list of descriptors to use for further
analysis.

Further summaries can be retrieved, for instance summaries at the
inventory classification level of detail can be quite useful when
exploring inventory policies:

.. code:: python

    classification_summary =  [summary for summary in filtered_summary.abc_xyz_summary(classification=('AY',), category=('revenue',))]
    print(classification_summary)


.. parsed-literal::

    [{'AY': {'revenue': 5372496600.0}}]


Now we know the total revenue generated by the ``AY`` SKU class. There
is another, slightly more fun way to arrive at this number using
``Dash`` but more on that latter.

.. code:: python

    top_10_safety_stock_skus =  [summary.get('sku')for summary in filtered_summary.rank_summary(attribute='safety_stock', count=10)]
    print(top_10_safety_stock_skus)


.. parsed-literal::

    ['KR202-241', 'KR202-231', 'KR202-233', 'KR202-227', 'KR202-225', 'KR202-212', 'KR202-240', 'KR202-244', 'KR202-236', 'KR202-211', 'KR202-243']


Lets add the safety\_stock and create a tuple to see that the results
explicitly.

.. code:: python

    top_10_safety_stock_values =  [(summary.get('sku'), summary.get('safety_stock'))for summary in filtered_summary.rank_summary(attribute='safety_stock', count=10)]
    print(top_10_safety_stock_values)


.. parsed-literal::

    [('KR202-241', '2719'), ('KR202-231', '2484'), ('KR202-233', '2472'), ('KR202-227', '2277'), ('KR202-225', '2261'), ('KR202-212', '2164'), ('KR202-240', '2120'), ('KR202-244', '2054'), ('KR202-236', '2045'), ('KR202-211', '2020'), ('KR202-243', '1954')]


We can then pass back the list of ``top_10_safety_stock_skus`` back into
the inventory filter and get their breakdown.

.. code:: python

    top_10_safety_stock_summary = [summary for summary in filtered_summary.describe_sku(*top_10_safety_stock_skus)]
    #print(top_10_safety_stock_summary)

We have only covered a few use cases but we have already achieved a
significant amount of analysis with relativley few line of code. The
equivalent in Excel would require much more work and many more formulas.
