# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging

from scipy import stats

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class LinearRegression:
    """ Linear Regression Statistics
    """
    def __init__(self, orders: list):
        self.orders = orders

    def least_squared_error(self, slice_end:int = 0, slice_start: int=0):
        """Calculate simple linear regression values and two_tail pvalue to determine linearity.

        Args:
            slice_end:      Start value for slicing the orders list. Default value is zero.
            slice_start:    End value for slicing the orders list. Default value is Zero. The length of the orders list
                            as supplied to the constructor is then used as the length of the orders.

        Returns:
            dict:           Regression results.

        Examples:
        >>> from supplychainpy.demand._forecast_demand import Forecast
        >>> orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147,
        ...           188, 161, 162, 169, 185, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218,
        ...           264, 304]
        >>> total_orders = 0
        >>> for order in orders[:12]:
        >>>     total_orders += order
        >>> avg_orders = total_orders / 12
        >>> forecasting_demand = Forecast(orders, avg_orders)
        >>> forecast = [i for i in forecasting_demand.simple_exponential_smoothing(0.5)]
        >>> regression = LinearRegression(forecast)
        >>> regression_statistics = regression.least_squared_error()
        """

        pvalue = 0.00
        slope = 0.00
        test_statistic = 0.00
        intercept = 0.00
        slope_standard_error = 0.00
        std_residuals = 0.00
        trend = False

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

            if pvalue < 0.05:
                trend = True
            else:
                trend = False

        except ValueError as e:
            log.debug('The value supplied to slice the orders list is out of range. {}'.format(e))
            print('Please review the range of orders requested. The current length of the orders is {}. '
                  'Please supply a range within this length.'.format(len(self.orders)))

        return {'slope': slope, 'pvalue': pvalue, 'test_statistic': test_statistic,
                'slope_standard_error': slope_standard_error, 'intercept': intercept,
                'std_residuals': std_residuals, 'trend': trend}
