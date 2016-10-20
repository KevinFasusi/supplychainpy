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

from decimal import Decimal, getcontext, ROUND_HALF_UP

import pyximport

from supplychainpy.inventory import analyse_uncertain_demand

#pyximport.install()
from supplychainpy.inventory.eoq import minimum_variable_cost
from supplychainpy.inventory.eoq import economic_order_quantity


class EconomicOrderQuantity:
    __economic_order_quantity = Decimal(0)
    analyse_uncertain_demand.UncertainDemand.__reorder_cost = Decimal(0)
    __holding_cost = Decimal(0)
    __min_variable_cost = Decimal(0)
    __reorder_quantity = Decimal(0)
    __unit_cost = 0.00

    @property
    def minimum_variable_cost(self) -> Decimal:
        return self.__min_variable_cost

    @property
    def economic_order_quantity(self) -> Decimal:
        return self.__economic_order_quantity

    def __init__(self, reorder_quantity: float, holding_cost: float, reorder_cost: float, average_orders: float,
                 unit_cost: float, total_orders: float):
        getcontext().prec = 8
        getcontext().rounding = ROUND_HALF_UP
        self.__reorder_quantity = Decimal(reorder_quantity)
        self.__holding_cost = holding_cost
        self.__reorder_cost = reorder_cost
        self.__unit_cost = unit_cost
        self.__min_variable_cost = minimum_variable_cost(total_orders, reorder_cost, unit_cost, holding_cost)
        self.__economic_order_quantity = economic_order_quantity(total_orders, reorder_cost, unit_cost, holding_cost,
                                                                 reorder_quantity)


