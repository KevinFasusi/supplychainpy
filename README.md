[![Build Status](https://travis-ci.org/KevinFasusi/supplychainpy.svg?branch=master)](https://travis-ci.org/KevinFasusi/supplychainpy?branch=master)
[![Documentation Status](https://readthedocs.org/projects/supplychainpy/badge/?version=latest)](http://supplychainpy.readthedocs.org/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/KevinFasusi/supplychainpy/badge.svg?branch=master)](https://coveralls.io/github/KevinFasusi/supplychainpy?branch=master)
[![PyPI version](https://badge.fury.io/py/supplychainpy.svg)](https://badge.fury.io/py/supplychainpy)
[![Requirements Status](https://requires.io/github/KevinFasusi/supplychainpy/requirements.svg?branch=master)](https://requires.io/github/KevinFasusi/supplychainpy/requirements/?branch=master)
![Supplychainpy logo](https://github.com/KevinFasusi/supplychainpy/blob/master/supplychainpy/reporting/static/images/logo-trn.png)

# Supplychainpy

Supplychainpy is a Python library for supply chain analysis, modelling and simulation. The library assists a workflow that is reliant on Excel and VBA.
Quite often Demand Planners, Buyers, Supply Chain Analysts and BI Analysts have to create their tools in Microsoft Excel for one reason or another. 
In a perfect world, the ERP/MRP system would be sufficient, but this is not always the case. Some issues include:

- Building reports and performing demand forecasts or planning inventory can become repetitive. 
- Visualisation tools are often platform dependent. 

It is the aim of this library to:

- Alleviate the reliance on Excel.
- Free up the analysts from some of the most mundane tasks of building tools.
- Provide a space for innovation and implementing advancements in the domain.
- Leverage the robust and extensible Python ecosystem.

The library is currently in early stages of development, so not ready for use in production. For quick exploration, please see the **Quick Guide** below.

## Quick Install

The easiest way to install supplychainpy is via pip: `pip install supplychainpy`.

An alternative is to clone the repository:

1. Run the command: `python setup.py sdist` 

2. Navigate to the `dist` folder.

3. Run the command: `pip install supplychainpy-0.0.4.tar.gz`


## Dependencies

- Numpy
- Pandas
- Flask
- Flask-Restful
- Flask-Restless
- Flask-Script
- Flask-SqlAlchemy
- Flask-Uploads
- Flask-WTF
- Scipy
- SqlAlchemy
- TextBlob


## Optional Dependencies

- matplotlib
- xlwings
- openpyxl


## Python Version

- python 3.5

## Quick Guide

Below is a quick example using a [sample data file](https://github.com/KevinFasusi/supplychainpy/blob/master/supplychainpy/sample_data/complete_dataset_small.csv). 

```python
    
from supplychainpy.model_inventory import analyse
from supplychainpy.sample_data.config import ABS_FILE_PATH
from decimal import Decimal

analysed_data = analyse(
						file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
						z_value=Decimal(1.28),
                        reorder_cost=Decimal(400),
                        retail_price=Decimal(455),
                        file_type='csv',
                        currency='USD'
                        )
analysis = [demand.orders_summary() for demand in analysed_data] 
```

output:

```
{'reorder_level': '4069', 'orders': {'demand': ('1509', '1855', '2665', '1841', '1231', '2598', '1988', '1988', '2927', '2707', '731', '2598')}, 'total_orders': '24638', 'economic_order_quantity': '44', 'sku': 'KR202-209', 'unit_cost': '1001', 'revenue': '123190000', 'quantity_on_hand': '1003', 'shortages': '5969', 'excess_stock': '0', 'average_orders': '2053.1667', 'standard_deviation': '644', 'reorder_quantity': '13', 'safety_stock': '1165', 'demand_variability': '0.314', 'ABC_XYZ_Classification': 'BY', 'economic_order_variable_cost': '15708.41', 'currency': 'USD'} ...
```


Alternatively using a Pandas `DataFrame`:

```python

from supplychainpy.model_inventory import analyse
from supplychainpy.sample_data.config import ABS_FILE_PATH
from decimal import Decimal
import pandas as pd

raw_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
analyse_kv = dict(
					df=raw_df,
        			start=1,
        			interval_length=12,
        			interval_type='months',
        			z_value=Decimal(1.28),
        			reorder_cost=Decimal(400),
			        retail_price=Decimal(455),
        			file_type='csv',
        			currency='USD'
        			)

analysis_df = analyse(**analyse_kv)

```


Further examples please refer to the jupyter notebooks [here](https://github.com/KevinFasusi/supplychainpy_notebooks).
For more detailed coverage of the api please see the [documentation](http://supplychainpy.readthedocs.org/).

## New Reporting Feature

The reports include a dashboard, raw analysis, a recommendations feed and SKU level analysis with forecast:

![reports](https://github.com/supplybi/supplybi.github.io/blob/master/images/reports.gif)


Launch reports can be achieved from the command line by:

```
    supplychainpy data.csv -a -loc absolute/path/to/current/directory -l
```

Other optional arguments include the host (--host default: 127.0.0.1 ) and port (-p default: 5000) arguments. Setting the host and ports allows the `-l` arguments can be replaced by the `-lx`. The `-l` arguments launch a small intermediary GUI for setting the port before launching the reports in a web browser. The `-lx` argument start the reporting process but does not launch a GUI or a browser window and instead expects the user to open the browser and navigate to the address hosting the reports as specified in the CLI. Another important flag is the currency flag (-cur) if unspecified, the currency is set to USD.

### ChatBot

The reporting suite also features a chatbot for querying the analysis in natural language. This feature is still under development, but a version is available in 0.0.4 (not yet released).

![chatbot](https://github.com/supplybi/supplybi.github.io/blob/master/images/dash.gif)

For a more detailed breakdown of the reporting features, please navigate to the [documentation](http://supplychainpy.readthedocs.org/) 

## Docker Image

The docker image for supplychainpy is built from the `continuumio/anaconda3` image, with a pre-installed version of supplychainpy and all the dependencies (see the [dockerfile](https://github.com/KevinFasusi/supplychainpy/blob/master/Dockerfile) for more).

```
    docker run -ti -v directory/on/host:directory/in/container --name fruit-smoothie -p5000:5000 supplychainpy/suchpy bash
```

The port, container name and directories can be changed as needed. Use a shared volume (as shown above) to present a CSV to the container for generating the report.

Make sure you specify the host as "0.0.0.0" for the reporting instance running in the container.

```
    supplychainpy data.csv -a -loc / -lx --host 0.0.0.0
```

## Important Links

- Jupyter Notebooks: [supplychainpy_notebooks](https://github.com/KevinFasusi/supplychainpy_notebooks)
- Documentation: [supplychainpy.readthdocs](http://supplychainpy.readthedocs.org/)
- Website: [supplychainpy.org](http://www.supplychainpy.org/)
- Forum: [google groups](https://groups.google.com/forum/#!forum/supplychainpy)

## License

BSD-3-Clause


## Change Log

### 0.0.5

**Application**

-   **[Bug Fix]** Using Flask's web server for the Dashboard on a public route on a standalone server (--host 0.0.0.0)
-   **[Bug Fix]** Javascript error while loading dashboard.
-   **[New]** Basic ability to run Monte Carlo Simulation and view summarised results in reporting suite.
-   **[Update]** Load scripts use multi-processing for forecast calculations when processing data file.
-   **[Update]** Load scripts using batch process.
-   **[Update]** Debug commandline argument for viewing logging output `--debug'.
-   **[Update]** Use Chat Bot from commandline with `-c` flag. EXPERIMENTAL
-   **[Update]** Recommendation generator takes into account forecasts
-   **[Update]** Flask Blueprints used for reporting views.


**Documentation**

-   **[New]** Wiki started on GitHub for more responsive updates to documentation including changes to source during development.
-   **[Update]** Tutorial.


### 0.0.4 [17 Nov 2016]

Release 0.0.4 has breaking API changes. Namespaces have changed in this release. All the modules previously in the
"demand" package are now inside the "inventory" package. If you have been using the "model_inventory" module, then nothing has
changed, there will not be any break in contracts.

#### Application

-   **[New]** Analytic Hierarchy Process.
-   **[New]** API supports Pandas `DataFrame`.
-   **[New]** Browser based reporting suite, with charts, data summaries and integrated chat bot.
-   **[New]** Dash Bot, a basic chat bot assistant for the data in the reporting suite. Query data using natural language.
-   **[New]** Command line interface for processing .csv to database, launching reports and chat bot.
-   **[New]** "Model_Demand" module containing simple exponential smoothing and holts trend corrected exponential smoothing.
-   **[New]** Summarise and filter your analysis.
-   **[New]** Holts Trend Corrected Exponential Smoothing Forecast and optimised variant (evolutionary algorithm for optimised alpha and gamma)
-   **[New]** Simple Exponential Smoothing (evolutionary algorithm for optimised alpha).
-   **[New]** Evolutionary Algorithms for Smoothing Level Constants (converges on better smoothing levels using genetic algorithm)
-   **[New]** SKU and inventory profile recommendations generator.
-   **[Update]** Explicit internal and public API.
-   **[Update]** Excess, shortages added to the UncertainDemand order_summary.
-   **[Update]** Moved abc_xyz.py, analyse_uncertain_demand.py, economic_order_quantity.py and eoq.pyx from "demand" to "inventory" package
-   **[Update]** "demand" package now contains: evolutionary_algorithms.py, forecast_demand.py and regression.py
-   **[Update]** retail_price added to `model_inventory.analyse_orders`.
-   **[Update]** backlog added to the data format for loading into the analysis.
-   **[Update]** Unit Tests.
-   **[Update]** Docstrings.

#### Documentation

-   **[New]** Reporting Suite Walk Through.
-   **[New]** Declare public API explicitly. describe and document each module and function, give an example also add to website tutorial as Jupyter notebook.
-   **[New]** Docker for supplychainpy quick guide.
-   **[New]** Analytic Hierarchy Process quick guide.
-   **[New]** Inventory Modeling.
-   **[New]** Demand Planning with Pandas.
-   **[Update]** Tutorial.
-   **[Update]** Quick Guide.

### 0.0.3 [30 Mar 2016]

**Application**

-  **[Update]** Compiled Cython (eoq and simulation modules) for OS X, Windows and Linux.
-  **[Update]** Removed z_value, file_type, file_path and reorder_cost parameters from simulate.run_monte_carlo.

**Documentation**

-  **[Update]** Quick Guide


### 0.0.2 [30 Mar 2016]

**Application**

-   **[New]** monte carlo simulation and simulation summary using Cython optimisation.
-   **[New]**  orders analysis optimisation, based on results of the monte carlo simulation.
-   **[New]**  simulate module to api.
-   **[New]**  weighted moving average forecast.
-   **[New]**  moving average forecast.
-   **[New]**  mean absolute deviation.
-   **[Update]** economic order quantity using Cython optimisation.
-   **[Update]** unit tests.

**Documentation**

-   **[New]** Formulas and Equations.
-   **[Update]** Quick Guide.
-   **[Update]** Tutorial.
-   **[Update]** README.md
-   **[Update]** updated data.csv.


## 0.0.1 [20 Feb 2016]

**Application**

-   **[New]** inventory analysis for uncertain demand. Analyse orders from .csv, .txt or from dict.
-   **[New]** inventory analysis summary for uncertain demand. ABC XYZ, economic order quantity (EOQ), reorder level (ROL), demand variability and safety stock.

**Documentation**

-   **[New]** Quick Guide.
-   **[New]** Tutorial.
-   **[New]** Installation.