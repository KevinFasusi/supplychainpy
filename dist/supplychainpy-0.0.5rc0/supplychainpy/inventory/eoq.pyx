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

from math import sqrt

# return a tuple for variable cost and order quantity without sending
def minimum_variable_cost(double total_orders, double  reorder_cost, double unit_cost, double  holding_cost):

    cdef double STEP
    STEP = 0.2
    cdef double previous_eoq_variable_cost

    cdef double vc
    cdef int counter = 0
    cdef double order_qty

    previous_eoq_variable_cost = 0.0
    vc = 0.0
    while previous_eoq_variable_cost >= vc:

        previous_eoq_variable_cost = vc
        # reorder cost * average demand all divided by order size + (demand size * holding cost)
        if counter < 1:
            order_qty = order_size(total_orders, reorder_cost, unit_cost, holding_cost)

        vc = variable_cost(total_orders, reorder_cost, order_qty, unit_cost, holding_cost)

        order_qty += order_qty * STEP

        if counter < 1:
            previous_eoq_variable_cost = vc

        while counter == 0:
            counter += 1

    return previous_eoq_variable_cost


def economic_order_quantity(double total_orders, double reorder_cost, double unit_cost, double holding_cost,
                            int reorder_quantity):

        cdef double STEP
        STEP= 0.2

        cdef double previous_eoq_variable_cost
        cdef double order_factor
        cdef double eoq_variable_cost

        cdef int counter = 0
        cdef double order_qty

        eoq_variable_cost = 0.0
        previous_eoq_variable_cost = 0.0

        while previous_eoq_variable_cost >= vc:

            previous_eoq_variable_cost = vc

            if counter < 1:
                order_qty = order_size(total_orders, reorder_cost, unit_cost, holding_cost)
                # print('1st order quantity {}'.format(order_qty))
            vc = variable_cost(total_orders, reorder_cost, order_qty, unit_cost, holding_cost)

            if counter >=1 :
                order_qty += order_qty * STEP

            if counter < 1:
                previous_eoq_variable_cost = vc

            while counter == 0:
                counter += 1

        return order_qty

cdef double variable_cost(double total_orders, double reorder_cost, double order_size, double  unit_cost,
                          double holding_cost):

    cdef double rc
    cdef double hc
    cdef double tvc

    rc = (total_orders * reorder_cost) / order_size
    hc = order_size * unit_cost * holding_cost
    tvc = rc + hc
    # print('reorder cost {}'.format(rc))
    # print('holding cost {}'.format(hc))
    # print('total variable cost {}'.format(tvc))
    return tvc

cdef double order_size(double total_orders, double  reorder_cost, double  unit_cost, double  holding_cost):

    cdef double order_qty

    order_qty = sqrt(((total_orders * reorder_cost * 2.0) / (unit_cost * holding_cost) ))* 0.4
    # print('order qty {}'.format(unit_cost * holding_cost))

    return order_qty

