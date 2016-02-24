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

Before we start, it is assumed you have a working installation of Python 3.5 and the supplychainpy library/

The command line (cli)
^^^^^^^^^^^^^^^^^^^^^^

The biggest difference across platforms will be when using the cli. For Mac and linux the unix shell and PC the command
prompt or PowerShell.

1. Create and save an Excel file on your desktop titled `test.xlsx`. Leave the workbook open.

2. The `data.csv` file is packaged with supplychainpy. We will use this file as the data source.

2. Fire up the terminal:


Mac

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

While several IDE's exist that can support this choice, it is the least favourable when working with Excel work


Ipython
^^^^^^^

The ipython notebook has many advantages including a consistent interface across both Mac and PC, easy saving of
notebooks and ability to share your work in various formats to name a few.

If you are unfamiliar with ipython and the suite of data analysis tools presented in the optional dependencies then
useful tools include: their respective websites, their documentation and the book
`Data Analysis <Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython>`_ by publisher O'Reilly.
The book is in its 1st edition (1 Nov 2012) but still very relevant and useful.

Fire up the unix

Inventory Analysis Example
==========================

Calculating the critical values for inventory analysis using a spreadsheet, often requires several steps. Extracting
transforming and loading (ETL) data, writing formulas, manual processes or pivot tables and in some cases vba. This
process is time consuming, repetitive, does not scale and could benefit from automation. Often the ETL is the first
part of that gets automated, while the rise in self service business intelligence tools assist a comprehensive library
in a productive language is a useful middle ground. Supplychainpy, Python and the expansive libraries fulfils the niche
for rolling out a scalable and automated suite of analysis.

Inventory Analysis
------------------


The inventory analysis functions can be accessed from supplychainpy by importing `model_inventory`.


Demand Planning and Forecasting
===============================



Warehousing
===========


Picking and Packing
-------------------


Distribution Optimisation
=========================


Simulation
==========

Monte Carlo simulation
----------------------

Agent based modeling
--------------------







