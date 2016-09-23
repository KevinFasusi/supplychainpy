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

from decimal import Decimal


class MonteCarloSummary:
    """
    """
    _opening_stock_average = 0.0
    _opening_stock_min = 0.0
    _opening_stock_max = 0.0
    _opening_stock_final = 0.0
    _opening_stock_std = 0.0
    _closing_stock_average = 0.0
    _closing_stock_min = 0.0
    _closing_stock_max = 0.0
    _closing_stock_final = 0.0
    _closing_stock_std = 0.0
    _stock_out_probability = 0.0
    _negative_stock_probabilit = 0.0
    _stock_out_count = 0.0

    def __init__(self):
        pass


    @property
    def opening_stock_final(self):
        return self._opening_stock_final

    @opening_stock_final.setter
    def opening_stock_final(self, opening_stock_final: Decimal):
        self._opening_stock_final = opening_stock_final

    @property
    def opening_stock_average(self):
        return self._opening_stock_average

    @opening_stock_average.setter
    def opening_stock_average(self, opening_stock_average: Decimal):
        self._opening_stock_average = opening_stock_average

    @property
    def opening_stock_min(self):
        return self._opening_stock_min

    @opening_stock_min.setter
    def opening_stock_min(self, opening_stock_min: Decimal):
        self._opening_stock_min = opening_stock_min

    @property
    def opening_stock_max(self):
        return self._opening_stock_max

    @opening_stock_max.setter
    def opening_stock_max(self, opening_stock_max: Decimal):
        self._opening_stock_max = opening_stock_max

    @property
    def opening_stock_std(self):
        return self._opening_stock_std

    @opening_stock_std.setter
    def opening_stock_std(self, opening_stock_std: Decimal):
        self._opening_stock_std = opening_stock_std

    @property
    def closing_stock_average(self):
        return self._closing_stock_average

    @closing_stock_average.setter
    def closing_stock_average(self, closing_stock_average: Decimal):
        self._closing_stock_average = closing_stock_average

    @property
    def closing_stock_min(self):
        return self._closing_stock_min

    @closing_stock_min.setter
    def closing_stock_min(self, closing_stock_min: Decimal):
        self._closing_stock_min = closing_stock_min

    @property
    def closing_stock_max(self):
        return self._closing_stock_max

    @closing_stock_max.setter
    def closing_stock_max(self, closing_stock_max: Decimal):
        self._closing_stock_max = closing_stock_max

    @property
    def closing_stock_std(self):
        return self._closing_stock_std

    @closing_stock_std.setter
    def closing_stock_std(self, closing_stock_std: Decimal):
        self._closing_stock_std = closing_stock_std

    @property
    def closing_stock_final(self):
        return self._closing_stock_final

    @closing_stock_final.setter
    def closing_stock_final(self, closing_stock_final: Decimal):
        self._closing_stock_final = closing_stock_final

