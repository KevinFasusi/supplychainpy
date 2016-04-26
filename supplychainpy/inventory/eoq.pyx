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

