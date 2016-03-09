
def minimum_variable_cost(double average_orders, double reorder_cost, double unit_cost, double holding_cost):

    cdef float STEP
    cdef float *increment_step = &STEP
    STEP[0] = 0.2

    cdef double previous_eoq_variable_cost
    cdef double order_factor = 0.002

    cdef double vc
    cdef int counter
    cdef double  order_size

    while previous_eoq_variable_cost >= vc:

        previous_eoq_variable_cost = vc
        # reorder cost * average demand all divided by order size + (demand size * holding cost)
        if counter < 1:
            order_size = order_size(average_orders=average_orders, reorder_cost=reorder_cost,
                                          unit_cost=unit_cost, holding_cost=holding_cost,
                                          order_factor=order_factor)
        rc = lambda x, y, z: (x * y) / z
        hc = lambda x, y, z: x * y * z
        vc = rc(float(average_orders), float(reorder_cost), float(order_size)) + hc(float(unit_cost),
                                                                                float(order_size),
                                                                                float(holding_cost))

        order_size += int(float(order_size) * STEP)
        if counter < 1:
            previous_eoq_variable_cost = vc

        while counter == 0:
            counter += 1

    return previous_eoq_variable_cost