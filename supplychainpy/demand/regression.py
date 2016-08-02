import numpy as np

import pandas as pd


class LinearRegression:
    def __init__(self, orders: dict):
        self.orders = orders

    @property
    def SSE(self) -> dict:
        return self._sum_squared_errors()

    def _sum_squared_errors(self) -> dict:
        orders_list = [i for i in self.orders["demand"]]
        orders_series = pd.Series(orders_list, name='orders').astype(float)
        orders_series.plot(y='orders')
        mean_expected_value = np.mean(orders_series)
        squared_errors = pd.Series(mean_expected_value - orders_series) ** 2
        sse = np.sum(squared_errors)
        return {'SSE': sse, 'squared_errors': squared_errors}
