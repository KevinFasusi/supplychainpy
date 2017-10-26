Quick Guide
===========

.. warning::
    The library is currently under development and in planning stages. The library should not be used in
    production at this time.

Overview
--------

Supplychainpy is a Python library for supply chain analysis, modelling and simulation. The library assists a workflow that is reliant on spreadsheets.

This quick guide assumes analysts have the requisite domain knowledge, and predominantly use Excel. Some
knowledge of Python or programming is assumed, although those new to data analysis or using Python will likely be able to
follow with assistance from other material.

The following guide assumes that the supplychainpy library has already been installed. If not, please use the
instructions for :ref:`installation`.

Up and Running
--------------

Typically, inventory analysis requires several formulas, manual processes, possibly some pivot tables and in
some cases VBA. Using the supplychainpy library can reduce the time taken and effort made for the same analysis.

A simple analysis for an individual SKU can be carried out by using:

.. code:: python

>>> from supplychainpy import model_inventory
>>> yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75,
>>>                 'may': 75, 'jun': 75, 'jul': 25,'aug': 25,
>>>                 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
>>> summary = model_inventory.analyse_orders(self._yearly_demand,  sku_id='RX983-90', lead_time= Decimal(3),
>>>                                             unit_cost=Decimal(50.99), reorder_cost=Decimal(400),
>>>                                             z_value=Decimal(1.28), retail_price=Decimal(600), quantity_on_hand=Decimal(390)))
>>> print(summary)


.. parsed-literal::

    {'revenue': '360000',
    'total_orders': '600',
    'orders': {'feb': 75, 'dec': 25, 'jan': 75, 'jun': 75, 'may': 75, 'mar': 75, 'aug': 25, 'sep': 25, 'jul': 25, 'oct': 25, 'nov': 25, 'apr': 75},
    'shortages': '0',
    'reorder_level': '142',
    'safety_stock': '55',
    'average_orders': '50',
    'standard_deviation': '25',
    'excess_stock': '161',
    'sku': 'RX983-90',
    'ABC_XYZ_Classification': '',
    'demand_variability': '0.500',
    'reorder_quantity': '56',
    'quantity_on_hand': '390',
    'currency': 'USD',
    'unit_cost': '50.99'}


.. note::  The signature for the `analysed_orders` function has changed. Moving from release-0.0.3 to release-0.0.4, **Retail price** and **quantity on hand** are required arguments.

The same analysis can be made by supplying a pre-formatted `.csv`, `.txt` or Pandas `DataFrame` containing several SKU or entire inventory profile. The format for the file can be found ` here <https://github.com/KevinFasusi/supplychainpy/blob/master/supplychainpy/sample_data/complete_dataset_small.csv>`_
An example using file:

.. code:: python

>>> from supplychainpy.model_inventory import analyse
>>> from supplychainpy.sample_data.config import ABS_FILE_PATH
>>> from decimal import Decimal
>>> analysed_data = analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
...                         z_value=Decimal(1.28),
...                         reorder_cost=Decimal(400),
...                         retail_price=Decimal(455),
...                         file_type='csv',
...                         currency='USD')
>>> analysis = [demand.orders_summary() for demand in analysed_data]


.. parsed-literal::

    {'quantity_on_hand': '1003',
    'currency': 'USD',
    'orders': {'demand': ('1509', '1855', '2665', '1841', '1231', '2598', '1988', '1988', '2927', '2707', '731', '2598')},
    'economic_order_variable_cost': '15708.41',
     'ABC_XYZ_Classification': 'BY',
     'reorder_level': '4069',
     'safety_stock': '1165',
     'shortages': '5969',
     'demand_variability': '0.314',
     'excess_stock': '0',
     'standard_deviation': '644',
     'average_orders': '2053.1667',
     'unit_cost': '1001',
     'economic_order_quantity': '44',
     'reorder_quantity': '13',
     'revenue': '123190000',
     'sku': 'KR202-209',
     'total_orders': '24638'},


The library also supports Pandas using a `DataFrame`. The following example shows how to use the library to perform an inventory analysis if a `DataFrame` is the preference:

.. code:: python

>>> import pandas as pd
>>> r_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
>>> analyse_kv = dict(
...     df=raw_df,
...     start=1,
...     interval_length=12,
...     interval_type='months',
...     z_value=Decimal(1.28),
...     reorder_cost=Decimal(400),
...     retail_price=Decimal(455),
...     currency='USD'
... )
>>> analysis_df = analyse(**analyse_kv)

Summarising the Analysis
^^^^^^^^^^^^^^^^^^^^^^^^
     
Use the `describe_sku` method a retrieve a summary for a specific skus:

.. code::

>>> from supplychainpy.inventory.summarise import Inventory
>>> from supplychainpy.model_inventory import analyse
>>> from supplychainpy.sample_data.config import ABS_FILE_PATH
>>> from decimal import Decimal
>>> analysed_data = analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
...                         z_value=Decimal(1.28),
...                         reorder_cost=Decimal(400),
...                         retail_price=Decimal(455),
...                         file_type='csv',
...                         currency='USD')
>>> filtered_summary = Inventory(processed_orders=analysed_orders)
>>> sku_summary = [summary for summary in filtered_summary.describe_sku('KR202-209')]
>>> print(sku_summary)



.. parsed-literal::

    {'economic_order_quantity': '44',
    'ABC_XYZ_Classification': 'BY',
    'sku': 'KR202-209',
    'shortages': '5969',
    'demand_variability': '0.314',
    'reorder_level': '4069',
    'reorder_quantity': '13',
    'unit_cost': '1001',
    'currency': 'UNKNOWN',
    'standard_deviation': '644',
    'revenue': '123190000',
    'average_orders': '2053.1667',
    'safety_stock': '1165',
    'quantity_on_hand': '1003',
    'orders': {'demand': ('1509', '1855', '2665', '1841', '1231', '2598', '1988', '1988', '2927', '2707', '731', '2598')},
    'excess_stock': '0',
    'economic_order_variable_cost': '15708.41',
    'total_orders': '24638'}

For more coverage of the library please take a look at the Jupyter notebooks is available from `here <https://github.com/KevinFasusi/supplychainpy_notebooks>`_ .
The content of notebooks can be found in :ref:`inventory` and :ref:`demand`.