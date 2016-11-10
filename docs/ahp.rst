Analytic Hierarchy Process
==========================

As of release 0.0.4, Supplychainpy will have the facility for computing the AHP of a given set of criteria and alternative options.
For an overview of the process, please visit this blog `post <http://www.supplychainpy.org/2016/10/26/Analytic-Hierarchy.html>`_

Below is a code snippet for the AHP:

.. code:: python

>>> from supplychainpy.model_decision import analytical_hierarchy_process
>>> lorry_cost = {'scania': 55000, 'iveco': 79000, 'volvo': 59000, 'navistar': 66000}
>>> criteria = ('style', 'reliability', 'comfort', 'fuel_economy')
>>> criteria_scores = [ (1 / 1, 2 / 1, 7 / 1, 9 / 1), (1 / 2, 1 / 1, 5 / 1, 5 / 1), (1 / 7, 1 / 5, 1 / 1, 5 / 1),(1 / 9, 1 / 5, 1 / 5, 1 / 1)]
>>> options = ('scania', 'iveco', 'navistar', 'volvo' )
>>>	option_scores = {
>>> 'style': [(1 / 1, 1 / 3, 5 / 1, 1 / 5), (3 / 1, 1 / 1, 2 / 1, 3 / 1), (1 / 3, 1 / 5, 1 / 1, 1 / 5), (5 / 1, 1 / 3, 5 / 1, 1 / 1)],
>>> 'reliability': [(1 / 1, 1 / 3, 3 / 1, 1 / 7), (3 / 1, 1 / 1, 5 / 1, 1 / 5), (1 / 3, 1 / 5, 1 / 1, 1 / 5), (7 / 1, 5 / 1, 5 / 1, 1 / 1)],
>>> 'comfort': [(1 / 1, 5 / 1, 5 / 1, 1 / 7), (1 / 5, 1 / 1, 2 / 1, 1 / 7), (1 / 3, 1 / 5, 1 / 1, 1 / 5), (7 / 1, 7 / 1, 5 / 1, 1 / 1)],
>>> 'fuel_economy': (11, 9, 10, 12)}
>>> lorry_decision = analytical_hierarchy_process(criteria=criteria,
...                                          criteria_scores=criteria_scores,
...                                          options=options,
...                                          option_scores=option_scores,
...                                          quantitative_criteria=('fuel_economy',),
...                                          item_cost=lorry_cost)

The results of the AHP:

.. parsed-literal::

    {'analytical_hierarchy': {'iveco': 0.20541585500041709, 'scania': 0.21539971200341132, 'volvo': 0.5677817531137912, 'navistar': 0.011402679882380324}, 'cost_benefit_ratios': {'iveco': 0.67345198031782316, 'scania': 1.0143368256160643, 'volvo': 2.4924656619741006, 'navistar': 0.044746880144492483}
