from scipy import stats
from scipy.stats.stats import ttest_ind

import numpy as np

import pandas as pd


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

    def least_squared_error(self):
        x_y_values = {}
        for i in self.orders:
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
        pvalue = stats.t.sf(abs(test_statistic), n-2) * 2
        return {'slope': slope, 'pvalue': pvalue, 'test_statistic': test_statistic,
                'slope_standard_error': slope_standard_error, 'intercept': intercept,
                'std_residuals': std_residuals}
