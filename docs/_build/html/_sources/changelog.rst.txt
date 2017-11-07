Change Log
==========

0.0.5
-----

Application
^^^^^^^^^^^
-   [Bug Fix] Using Flask's web server for the Dashboard on a public route on a standalone server (--host 0.0.0.0)
-   [Bug Fix] Javascript error while loading dashboard.
-   [Bug Fix] Pip install error (Log.txt FileNotFound)
-   [New Feature] Basic ability to run Monte Carlo Simulation and view summarised results in reporting suite.
-   [Update] Load scripts use multi-processing for forecast calculations when processing data file.
-   [Update] Load scripts using batch process.
-   [Update] Debug commandline argument for viewing logging output `--debug'.
-   [Update] Use Chat Bot from commandline with `-c` flag. EXPERIMENTAL
-   [Update] Recommendation generator takes into account forecasts
-   [Update] Flask Blueprints used for reporting views.


Documentation
^^^^^^^^^^^^^
-   [New] Wiki started on GitHub for more responsive updates to documentation including changes to source during development.
-   [Update] Tutorial.



0.0.4
-----
Release 0.0.4 has breaking API changes. Namespaces have changed in this release. All the modules previously in the
"demand" package are now inside the "inventory" package. If you have been using the "model_inventory" module, then nothing has
changed, there will not be any break in contracts.


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

Options
-----

Currently using the reporting suite feature, requires the command line. Using a nix or PowerShell console, the typical command issued for processing a file and generating a report would be:

`$ supplychainpy <filename> -a -loc <absolute-path-to-current-directory> -l`


The command line arguments can be viewed by using the `--help` command in the cli.

- `-l, --launch`

	- Launches supplychainpy reporting GUI for setting port and launching the default browser. The reporting suite is hosted inside the browser and defaults to port 5000. The GUI provides the opportunity to change the port if necessary. The `-l` flag is a boolean flag, and its inclusion is essential if the aim is to launch into the reporting suite.

- `-loc`

	- Flag for the aboslute path to the current directory. The path is required to locate a current reporting.db or a store as the new location in the settings.

-  `-a, --analyse`

	-  Initiates the analyisis of the file name supplied as the first argument directly after the `supplychainpy` command e.g.:

		`$ supplychainpy <filename> -a -loc <absolute-path-to-current-directory> -l`

- `-lx, --launch-console`

	- Launches supplychainpy reporting on the default port, without GUI interface. Uses default port (5000) unless another port is specified. Appropriate for running the reports on a sever. Currently, this is only for testing. The Werkzeug web server that supplied with flask serves the pages for the reports. Werkzeug is not a production web server. It is sufficient as a local web server for the reporting application on a client system. In the coming releases deployment using a more robust web server such as Nginx or Gunicorn will be documented for Server type implementation.

- `-cur`

	- The flag Sets the currency for the analysis and should match the raw data. IMPORTANT: Currency conversion does not occur by setting this flag. The default currency is US Dollars (USD).

- `--host`

	- Sets the host for the server (defaults 127.0.0.1).


- `--debug`

	- Runs in debug mode.


- `-p, --port`

	- Specify Port to use for local server e.g. 8080 (default: 5000).

- `-c`

	- Enter chat mode with the Dash bot from the command line.


