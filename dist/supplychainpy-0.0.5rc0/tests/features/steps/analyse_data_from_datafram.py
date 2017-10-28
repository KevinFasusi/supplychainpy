from _decimal import Decimal

from behave import *
from pandas import DataFrame
import pandas as pd

from supplychainpy.model_inventory import analyse
from supplychainpy.sample_data.config import ABS_FILE_PATH

use_step_matcher("re")

@given("I extract data from a CSV")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): 
    """
    raw_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
    context.response = raw_df


@when("I analyse raw data in a Pandas DataFrame")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): 
    """
    analyse_kv = dict(
        df=context.response,
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
    context.response = analysis_df



@then("It should return a DataFrame with Descriptive Statistics")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): 
    """
    assert isinstance(context.response, DataFrame)