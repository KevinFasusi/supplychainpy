Change Log
==========


0.0.4
-----
Release 0.0.4 has breaking API changes. Namespaces have changed in this release. All the modules previously in the
"demand" package are now inside the "inventory" package. If you have been using the "model_inventory" module, then nothing has
changed, and there will not be any break in contracts.


Application
^^^^^^^^^^^

-   [Update] Explicit internal and public API.
-   [Update] Excess, shortages added to the UncertainDemand order_summary.
-   [Update] Moved abc_xyz.py, analyse_uncertain_demand.py, economic_order_quantity.py and eoq.pyx from "demand" to "inventory" package
-   [Update] "demand" package now contains: evolutionary_algorithms.py, forecast_demand.py and regression.py
-   [Update] retail_price added to `model_inventory.analyse_orders`.
-   [Update] backlog added to the data format for loading into the analysis.
-   [Update] Unit Tests.
-   [Update] Docstrings.
-   [New Feature] Analytic Hierarchy Process.
-   [New Feature] API supports Pandas `DataFrame`.
-   [New Feature] Browser based reporting suite, with charts, data summaries and integrated chat bot.
-   [New Feature] Dash Bot, a basic chat bot assistant for the data in the reporting suite. Query data using natural language.
-   [New Feature] Command line interface for processing .csv to database, launching reports and chat bot.
-   [New Feature] "Model_Demand" module containing simple exponential smoothing and holts trend corrected exponential smoothing.
-   [New Feature] Summarise and filter your analysis.
-   [New Feature] Holts Trend Corrected Exponential Smoothing Forecast and optimised variant (evolutionary algorithm for optimised alpha and gamma)
-   [New Feature] Simple Exponential Smoothing (evolutionary algorithm for optimised alpha).
-   [New Feature] Evolutionary Algorithms for Smoothing Level Constants (converges on better smoothing levels using genetic algorithm)
-   [New Feature] SKU and inventory profile recommendations generator.

Documentation
^^^^^^^^^^^^^

-   [New] Reporting Suite Walk Through.
-   [Update] Tutorial.
-   [Update] Quick Guide.
-   [New] Declare public API explicitly. describe and document each module and function, give an example also add to website tutorial as Jupyter notebook.
-   [New] Docker for supplychainpy quick guide.
-   [New] Analytic Hierarchy Process quick guide.
-   [New] Inventory Modeling.
-   [New] Demand Planning with Pandas.

0.0.3
-----

Application
^^^^^^^^^^^

-   Compiled Cython (eoq and simulation modules) for OS X, Windows and Linux.
-   Removed z_value, file_type, file_path and reorder_cost parameters from simulate.run_monte_carlo.

Documentation
^^^^^^^^^^^^^

-   Update Quick Guide

0.0.2
-----

Application
^^^^^^^^^^^

-   Added monte carlo simulation and simulation summary using Cython optimisation.
-   Added orders analysis optimisation, based on results of the monte carlo simulation.
-   Added simulate module to api.
-   Added weighted moving average forecast.
-   Added moving average forecast.
-   Added mean absolute deviation.
-   Updated economic order quantity using Cython optimisation.
-   Updated unit tests.

Documentation
^^^^^^^^^^^^^

-   Updates Quick Guide.
-   Updated Tutorial.
-   Updated README.md
-   Added Formulas and Equations.
-   Updated data.csv.

0.0.1
-----

Application
^^^^^^^^^^^

-   Added inventory analysis for uncertain demand. Analyse orders from .csv, .txt or from dict.
-   Added inventory analysis summary for uncertain demand. ABC XYZ, economic order quantity (EOQ), reorder level (ROL),
    demand variability and safety stock.

Documentation
^^^^^^^^^^^^^

-   Added Quick Guide.
-   Added Tutorial.
-   Added Installation.

