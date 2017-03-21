
Monte Carlo Simulation
----------------------

After analysing the orders, the results for safety stock may not adequately calculate
the service level required. The complexity of the supply chain operation may include randomness an analytical model
does not capture. A simulation is useful for giving a dynamic view of a complex process. The simulation replicates
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

The Monte Carlo simulation generates normally distributed random demand, based on the historical data. The demand for each SKU is then used in each period to model a probable transaction history. The output below are the sales for one SKU over the year for 100 runs (1 run shown).

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

After running the Monte Carlo simulation, the results can be passed as a parameter for summary:

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
run will have a different randomly generated demand. Due to the randomised demand, the transaction summary for the same SKU will differ over consecutive runs. The spread of data captures the statistically probable distribution of demand the SKU can expect. However the more runs (thousands, tens of thousands), the more useful the result.

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


The `summarize_window` returns max, min, averages and standard deviations for the primary values from the transaction summary.

The last method summarises the runs into one transaction summary for each SKU. Similar in content to the previous
summary, however, this summary aggregates the simulation runs.

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


Below is 1 of 32 results for 32 SKUs ran 100 times.

.. parsed-literal::

    {'standard_deviation_quantity_sold': '2228', 'average_backlog': '0', 'standard_deviation_closing_stock': '2228',
    'maximum_quantity_sold': 7901.0, 'sku_id': 'KR202-209', 'minimum_quantity_sold': 407.0, 'minimum_backlog': 0.0,
    'average_closing_stock': '3592', 'average_shortage_units': '0', 'variance_opening_stock': '2287',
    'minimum_opening_stock': 407, 'maximum_opening_stock': 7901, 'minimum_closing_stock': 407, 'service_level': '100.00',
    'maximum_closing_stock': 7901, 'average_quantity_sold': '3592', 'standard_deviation_backlog': '0',
    'maximum_backlog': 0.0}

An optimisation option exists, if after running the Monte Carlo analysis, the behaviour in the transaction summary is not favourable. If most SKUs are not achieving their desired service level or have large
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
reviewed and compared with the desired service level. If below a threshold, then the safety stock is increased, and the
full Monte Carlo simulation runs again. The supplied variable percentage_increase specifies the growth in safety stock.

This optimisation step will take as long, if not longer, than the first Monte Carlo simulation because the optimisation step runs the simulation again to simulate transactions based on the new safety stock values. Please take this into consideration and adjust your expectation for this optimisation step. This feature is in development as is the whole library but this feature will change in the next release.

For further details on the implementation, please view the `deep-dive blog posts <http://www.supplychainpy.org/blog/>`_
for each release.
