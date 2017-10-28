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

class MonteCarloFrameSummary:
    def __init__(self):
        pass

    @staticmethod
    def closing_stockout_percentage(closing_stock: list, period_length: int):
        """ Calculates the percentage of stock out that occurred during the period specified.


        Args:
            period_length (int):    length of window e.g. 12 weeks for a quarter etc.
            closing_stock (list):   list of closing stock values for a given sku over the same time frame
                                    as the period_length


        Returns:
            float:   Percentage of final closing stock values that result in stock out and backlog.

        Raises:
            ValueError: The number of stock positions and the period length must match exactly.
        """
        if len(closing_stock) != period_length:
            raise ValueError(" The number of stock positions and the period length must match exactly.\nThe"
                             " number of stock positions passed for closing stock is currently {}. "
                             "The length specified for period_length is currently {}".format(len(closing_stock),
                                                                                                 period_length))

        closing_stock_count = ([x for x in closing_stock if x <= 0])
        percentage = len(closing_stock_count) / period_length
        return percentage
