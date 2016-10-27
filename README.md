[![Build Status](https://travis-ci.org/KevinFasusi/supplychainpy.svg?branch=master)](https://travis-ci.org/KevinFasusi/supplychainpy?branch=master)
[![Documentation Status](https://readthedocs.org/projects/supplychainpy/badge/?version=latest)](http://supplychainpy.readthedocs.org/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/KevinFasusi/supplychainpy/badge.svg?branch=master)](https://coveralls.io/github/KevinFasusi/supplychainpy?branch=master)
[![PyPI version](https://badge.fury.io/py/supplychainpy.svg)](https://badge.fury.io/py/supplychainpy)

![Supplychainpy logo](https://github.com/KevinFasusi/supplychainpy/blob/master/supplychainpy/reporting/static/PY_logo.jpg)

# Supplychainpy

Supplychainpy is a Python library for supply chain analysis, modeling and simulation. The library is currently in early stages of development, so not ready for use in production. For quick exploration, please see the **Quick Guide** below.

## Quick Install

The easiest way to install supplychainpy is via pip: `pip install supplychainpy`.

An alternative is to clone the repository and run `python setup.py install`

## Dependencies

- Numpy
- Flask
- Flask-SqlAlchemy
- SqlAlchemy
- Flask-Restless
- TextBlob
- Pandas

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

Important Links:

- Jupyter Notebooks: [supplychainpy_notebooks](https://github.com/KevinFasusi/supplychainpy_notebooks)
- Documentation: [supplychainpy.readthdocs](http://supplychainpy.readthedocs.org/)
- Website: [supplychainpy.org](http://www.supplychainpy.org/)
- Forum: [google groups](https://groups.google.com/forum/#!forum/supplychainpy)




