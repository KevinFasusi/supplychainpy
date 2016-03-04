Supplychainpy, Xlwings, Pandas and Ipython Tutorial
===================================================

Supplychainpy is a Python library for supply chain analysis, modeling and simulation. Using the supplychainpy
with popular data analysis libraries and tools such as Xlwings or Data Nitro (for Excel spreadsheet applications),
Pandas, NumPy, Matplotlib, Ipython and Jupyters makes for a powerful supply chain data analysis toolchain.

Several libraries and technologies exist for interacting with Excel using Python. In this tutorial we use Xlwings
because it is freely available, packaged with Anaconda (see :ref:`Installation` for details), cross platform (working
on Mac and PC) and very well documented. The Xlwings project is also in active development, with continuous updates and
maintenance.

This tutorial is skewed towards analysts with the requisite domain knowledge, who predominantly use Excel. Some
knowledge of Python or programming is assumed, although those new to data analysis using python will likely be able to
follow with assistance from other material.

This tutorial will proceed to build a typical Excel workbook for inventory management for a fictitious original
equipment manufacturer (OEM). The examples will be as generic as possible, working exactly the same on both Mac and PC.
Should there be differences in implementation across both platforms, these differences will be explained.

Ipython, the command line (cli) or an integrated development environment (IDE)
------------------------------------------------------------------------------

Many choices are available for you when interacting with the workbook on your system. We will quickly explore all the
alternatives before continuing with our chosen interface the ipython notebook.

Before we start, it is assumed you have a working installation of Python 3.5, the supplychainpy library and Excel.

The command line (cli)
^^^^^^^^^^^^^^^^^^^^^^

The biggest difference across platforms will be when using the cli. For Mac and linux the unix shell and PC the command
prompt or PowerShell.

1. Create and save an Excel file on your desktop titled `test.xlsx`. Leave the workbook open.

2. The `data.csv` file is packaged with supplychainpy. We will use this file as the data source.

2. Fire up the terminal:


Mac and Pc (command prompt)

.. code:: bash

	python3

Now using the `data.csv` file and `test.xlsx` workbook, we can run our first analysis.

.. code:: python

	>>> from xlwings import Workbook, Range
	>>> from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
	>>> wb = Workbook(r'~/Desktop/test.xlsx'), Range
	>>> abc = analyse_orders_abcxyz_from_file(file_path="data.csv", z_value= Decimal(1.28), reorder_cost=Decimal(5000), file_type="csv")
	>>> x = 1
	>>> for sku in abc.orders:
	>>>     Range('A'+ str(x)).value = sku.sku_id
	>>>     Range('B' + str(x)).value = float(sku.economic_order_qty)
	>>>     Range('C' + str(x)).value = float(sku.revenue)
	>>>     Range('D' + str(x)).value = sku.abcxyz_classification
	>>>     x +=1

You should be able to see the following print out in

windows version


Now that you are sure you ave got this up and running you can continue and explore the libraries api using the
:ref:`modindex`. The main capabilities are discussed below.

2. and get ipython notebook up and running:


Integrated Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While several IDE's exist that can support this choice, it is the least favourable when working with Excel.


Ipython
^^^^^^^

The ipython notebook has many advantages including a consistent interface across both Mac and PC, easy saving of
notebooks and ability to share your work in various formats to name a few.

If you are unfamiliar with ipython and the suite of data analysis tools presented in the optional dependencies then
useful tools include: their respective websites, their documentation and the book
`Data Analysis <Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython>`_ by publisher O'Reilly.
The book is in its 1st edition (1 Nov 2012) but still very relevant and useful.


Inventory Analysis Example
==========================

Calculating the critical values for inventory analysis using a spreadsheet, often requires several steps. Extracting
transforming and loading (ETL) data, writing formulas, manual processes or pivot tables and in some cases vba. This
process is time consuming, repetitive, does not scale and could benefit from automation. Often the ETL is the first
part of to get automated, while the rise in self-service business intelligence tools help automate the reporting.
A comprehensive library in a productive language is a useful middle ground. Supplychainpy, Python and the extensive
python libraries hopefully fulfils the niche for rolling out a scalable and automated suite of analysis.

Inventory Analysis
------------------

The inventory analysis functions can be accessed from supplychainpy by importing `model_inventory`.



Simulation
==========

A method for checking the validity of the decisions made is useful for inventory managers to evaluate the appropriateness
of any changes.

A simulation is useful for giving a dynamic view of an operations system. The simulation replicates the complexity of the system
over time and captures randomness for a more accurate result. The monte carlo simulation is useful when complicated interactions
and effects are not adequately captured by an analytical model.


Monte Carlo simulation
----------------------

The code below returns the `transaction report` covering the number of periods specified, multiplied by the number of runs
requested. The higher the number of runs the more accurately the simulation captures the dynamics of the system limited by
the assumptions inherent in the simulations design.

.. code:: python

	>>> sim = simulate.run_monte_carlo(file_path="data.csv", z_value=Decimal(1.28), runs=1,
	>>> reorder_cost=Decimal(4000), file_type="csv", period_length=12)
	>>> for s in sim:
	>>>    print(s)

This is the output from 1 run for 1 sku. The demand is normal random distribution and the PO's raised

.. parsed-literal::

	[{'closing_stock': '690', 'sku_id': 'KR202-214', 'demand': '805', 'backlog': '0',
	'opening_stock': '1500', 'period': '1', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '-2600', 'sku_id': 'KR202-214', 'demand': '2023', 'backlog': '1300',
	'opening_stock': '690', 'period': '2', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '-2600', 'sku_id': 'KR202-214', 'demand': '1665', 'backlog': '1300',
	'opening_stock': '-2600', 'period': '3', 'index': '6', 'delivery': '3000'}]
	[{'closing_stock': '3500', 'sku_id': 'KR202-214', 'demand': '1501', 'backlog': '0',
	'opening_stock': '-2600', 'period': '4', 'index': '6', 'delivery': '7600'}]
	[{'closing_stock': '11000', 'sku_id': 'KR202-214', 'demand': '134', 'backlog': '0',
	'opening_stock': '3500', 'period': '5', 'index': '6', 'delivery': '7600'}]
	[{'closing_stock': '9600', 'sku_id': 'KR202-214', 'demand': '1611', 'backlog': '0',
	'opening_stock': '11000', 'period': '6', 'index': '6', 'delivery': '200'}]
	[{'closing_stock': '7100', 'sku_id': 'KR202-214', 'demand': '2525', 'backlog': '0',
	'opening_stock': '9600', 'period': '7', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '5800', 'sku_id': 'KR202-214', 'demand': '1318', 'backlog': '0',
	'opening_stock': '7100', 'period': '8', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '3700', 'sku_id': 'KR202-214', 'demand': '2097', 'backlog': '0',
	'opening_stock': '5800', 'period': '9', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '1100', 'sku_id': 'KR202-214', 'demand': '2612', 'backlog': '0',
	'opening_stock': '3700', 'period': '10', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '400', 'sku_id': 'KR202-214', 'demand': '695', 'backlog': '0',
	'opening_stock': '1100', 'period': '11', 'index': '6', 'delivery': '0'}]
	[{'closing_stock': '2400', 'sku_id': 'KR202-214', 'demand': '643', 'backlog': '0',
	'opening_stock': '400', 'period': '12', 'index': '6', 'delivery': '2600'}]


.. code:: python

	>>> for i in simulate.summarize_window(simulation_frame=sim, period_length=12):
	>>>    print(i)

.. parsed-literal::

	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.3333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.3333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.3333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.0, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.08333333333333333, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.25, 'index': '1'}
	{'sku_id': 'KR202-209', 'stockout_percentage': 0.16666666666666666, 'index': '1'}

Overview of simulation model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

insert flow diagram here.



Agent based modeling
--------------------



Demand Planning and Forecasting
===============================



Warehousing
===========


Picking and Packing
-------------------


Distribution Optimisation
=========================









