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
    analysed_data = analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                            z_value=Decimal(1.28),
                            reorder_cost=Decimal(400),
                            retail_price=Decimal(455),
                            file_type='csv',
                            currency='USD')
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

