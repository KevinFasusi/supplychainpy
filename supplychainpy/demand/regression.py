import logging

from scipy import stats
from scipy.stats.stats import ttest_ind

import numpy as np

import pandas as pd

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class LinearRegression:
    def __init__(self, orders: list):
        self.orders = orders

    @property
    def SSE(self) -> dict:
        return self._sum_squared_errors()

    def _sum_squared_errors(self) -> dict:
        orders_list = [i for i in self.orders]
        orders_series = pd.Series(orders_list, name='orders').astype(float)
        orders_series.plot(y='orders')
        mean_expected_value = np.mean(orders_series)
        squared_errors = pd.Series(mean_expected_value - orders_series) ** 2
        sse = np.sum(squared_errors)
        return {'SSE': sse, 'squared_errors': squared_errors}

    def least_squared_error(self, slice_end:int = 0, slice_start: int=0):
        """Calculate simple linear regression values and two_tail pvalue to determine linearity.

        Args:
            slice_end:      Start value for slicing the orders list. Default value is zero.
            slice_start:    End value for slicing the orders list. Default value is Zero. The length of the orders list
                            as supplied to the constructor is then used as the length of the orders.

        Returns:
            dict:           {'test_statistic': 7.267765176382303,
                            'intercept': 143.63697478991594,
                            'slope_standard_error': 0.298274237297937,
                            'slope': 2.1677871148459382,
                            'std_residuals': 1064.839027153635,
                            'pvalue': 2.4466485335258775e-08}}

        Examples:
                            orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147,
                            188, 161, 162, 169, 185, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218,
                            264, 304]
                            total_orders = 0
                            for order in orders[:12]:
                                total_orders += order
                            avg_orders = total_orders / 12
                            forecasting_demand = Forecast(orders, avg_orders)
                            forecast = [i for i in forecasting_demand.simple_exponential_smoothing(0.5)]
                            regression = LinearRegression(forecast)
                            regression_statistics = regression.least_squared_error()

        """

        pvalue = 0.00
        slope = 0.00
        test_statistic = 0.00
        intercept = 0.00
        slope_standard_error = 0.00
        std_residuals = 0.00

        try:
            if slice_end == 0 and slice_start == 0:
                slice_start, slice_end = 0, (len(self.orders) - 1)
            else:
                slice_start = slice_start
                slice_end = slice_end

            x_y_values = {}

            for i in self.orders[slice_start:slice_end]:
                x_y_values.update({i['t']: i['demand']})
            x_mul_y = {k: k * v for k, v in x_y_values.items()}
            x_sq = {k: k ** 2 for k in x_y_values.keys()}
            sum_x = sum([k for k in x_y_values.keys()])
            sum_y = sum([v for v in x_y_values.values()])
            sum_x_sq = sum([x for x in x_sq.values()])
            sum_x_mul_y = sum([v for v in x_mul_y.values()])
            total_sum_x_sq = sum_x ** 2
            total_sum_y_sq = sum_y ** 2
            n = len(x_y_values)
            slope = (n * (sum_x_mul_y) - (sum_x) * (sum_y)) / (n * (sum_x_sq) - total_sum_x_sq)
            intercept = (sum_y / n) - slope * (sum_x / n)
            std_residuals = ((total_sum_y_sq - intercept * sum_y - slope * sum_x_mul_y) / n - 2) ** 0.5
            ss = (sum_x_sq - (total_sum_x_sq) / n)
            slope_standard_error = std_residuals / ss
            test_statistic = slope / slope_standard_error
            pvalue = stats.t.sf(abs(test_statistic), n - 2) * 2

        except ValueError as e:
            log.debug('The value supplied to slice the orders list is out of range. {}'.format(e))
            print('Please review the range of orders requested. The current length of the orders is {}. '
                  'Please supply a range within this length.'.format(len(self.orders)))

        return {'slope': slope, 'pvalue': pvalue, 'test_statistic': test_statistic,
                'slope_standard_error': slope_standard_error, 'intercept': intercept,
                'std_residuals': std_residuals}
