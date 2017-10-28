import logging
from supplychainpy.simulations.simulation_window import MonteCarloWindow

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

cdef revenue(double unit_cost, double units_sold):
    return unit_cost * units_sold

cdef closing_stock(double backlog,  double opening_stock, double deliveries, double orders):
    if  (opening_stock - orders) + (deliveries) > 0:
        return ((opening_stock - orders) + deliveries) - backlog
    else:
        return 0

cdef backlog(double opening_stock, double deliveries, double demand):
    if ((opening_stock + deliveries) - demand) < 0 :
        return abs(opening_stock + deliveries) - demand
    else:
        return 0

cdef holding_cost(double closing_stock, double unit_cost, double holding_cost_percentage):
    if closing_stock > 0:
        return closing_stock * unit_cost * holding_cost_percentage
    else:
        return 0

cdef shortages(double opening_stock, double orders, double deliveries):
    if ((opening_stock - orders) + deliveries) < 0:
        return ((opening_stock - orders) + deliveries)
    else:
        return 0

cdef shortage_cost(double closing_stock, double unit_cost, double shortage_cost_percentage):
    if closing_stock > 0 :
        return closing_stock * (unit_cost * shortage_cost_percentage)
    else:
        return 0


cdef raise_po(double reorder_level, double closing_stock):
    return True if closing_stock <= reorder_level else False

cdef po_qty(double eoq, double reorder_level, double backlog, double closing_stock):
    if ((eoq + backlog + reorder_level) - closing_stock) > 0:
        return ((eoq + backlog + reorder_level) - closing_stock)
    else:
        return 0

cdef opening_stock(double reorder_level, double safety_stock, int position, double previous_closing_stock):
    if position == 1:
        stock = reorder_level #calculated ltd until put into analyse orders
    else:
        stock = previous_closing_stock
    return stock

cdef units_sold(double backlog, double opening_stock, double delivery, double demand):

    # check if opening_stock + closing_stock = 0
    if int(opening_stock) + int(delivery) == 0:
        sold = 0.00
    else:
        sold = (opening_stock + delivery) - demand - backlog

    if sold < 0:
        units_sold = demand + backlog - abs(sold)
    else:
        units_sold = sold

    return units_sold

cdef previous_backlog(double backlog, double closing_stock, double previous_backlog):
        if closing_stock == 0.00:
            previous_backlog += backlog
            return previous_backlog
        else:
            return 0

def simulation_window(list random_normal_demand, int period_length, list analysed_orders,
                     double holding_cost_percentage = 0.48,
                     double shortage_cost_percentage = 0.3):


    for sku in analysed_orders:
        if period_length != len(random_normal_demand[0][sku.sku_id]):
            raise ValueError("The period_length is currently {} and the actual length of the demand is {}. "
                             "Please make sure that the two values are equal".format(period_length,
                                                                                     len(random_normal_demand[0][
                                                                                             sku.sku_id])))

    cdef list sim_frame_collection = []
    cdef int index_item = 1
    cdef int period = 1
    cdef dict order_receipt_index
    cdef double final_stock = 0.0
    cdef dict sim_window_collection = {}
    cdef int po_qty_raised
    cdef double sold
    for sku in analysed_orders:

        period = 1
        order_receipt_index = {}
        final_stock = 0
        sim_window_collection = {}
        order_receipt_index = {}

        # create the sim_window for each sku, suing the random normal demand generated
        for i in range(0, period_length):

            po_qty_raised = 0
            #log.log(logging.INFO,'Current purchase order quantity {}'.format(po_qty_raised))

            # instantiate sim_window
            sim_window = MonteCarloWindow()

            # add sku_id
            sim_window.sku_id = sku.sku_id
            #log.log(logging.INFO,'Current SKU: {}'.format(sim_window.sku_id))
            # add closing stock
            previous_closing_stock = final_stock

            # mark sim_window.position or period in analysis
            sim_window.position = period

            #log.log(logging.INFO,('Current window position {}'.format(sim_window.position)))

            # add average orders to opening_stock if first period else add closing stock
            sim_window.opening_stock = opening_stock(sku.reorder_level, sku.safety_stock, sim_window.position,previous_closing_stock ) #calculated ltd until put into analyse orders

            # add random demand
            demand = random_normal_demand[0][sku.sku_id][i][0]
            sim_window.demand = demand
            #log.log(logging.INFO,('Current window demand {}'.format(sim_window.demand)))


            if sim_window.position in order_receipt_index.keys():
                sim_window.purchase_order_receipt_qty = order_receipt_index[sim_window.position]
                sim_window.po_number_received = 'PO {:.0f}{}'.format(sim_window.position, sim_window.index)
                del order_receipt_index[sim_window.position]
            else:
                sim_window.purchase_order_receipt_qty = 0
                sim_window.po_number_received = ''

            sim_window.index = index_item

            sim_window.backlog = backlog(opening_stock=sim_window.opening_stock,
                                         deliveries=sim_window.purchase_order_receipt_qty,
                                         demand=demand) + sim_window.previous_backlog

            sim_window.closing_stock = closing_stock(opening_stock=sim_window.opening_stock,
                                                     orders=demand,
                                                     deliveries=sim_window.purchase_order_receipt_qty,
                                                     backlog=sim_window.backlog)

            sim_window.holding_cost = holding_cost(sim_window.closing_stock, sku.unit_cost, holding_cost_percentage)

            sim_window.shortage_units = shortages(opening_stock=sim_window.opening_stock,
                                                  orders=demand,
                                                  deliveries=sim_window.purchase_order_receipt_qty)

            sim_window.shortage_cost = shortage_cost(closing_stock=(sim_window.backlog - sim_window.previous_backlog),
                                                     unit_cost=sku.unit_cost, shortage_cost_percentage=shortage_cost_percentage)

            sim_window.po_raised_flag = raise_po(reorder_level=sku.reorder_level, closing_stock=sim_window.closing_stock)

            po_receipt_period = period + sku.lead_time

            po_qty_raised = po_qty(eoq=sku.economic_order_qty,
                                   reorder_level=sku.reorder_level,
                                   backlog=sim_window.backlog,
                                   closing_stock=sim_window.closing_stock)

            if po_qty_raised > 0:
                order_receipt_index.update({po_receipt_period: po_qty_raised})
                sim_window.purchase_order_raised_qty = order_receipt_index.get(po_receipt_period)
            else:
                sim_window.purchase_order_raised_qty = 0

            sim_window.po_number_raised = ''

            if int(sim_window.purchase_order_raised_qty) > 0:
                sim_window.po_number_raised = 'PO {:.0f}{}'.format(po_receipt_period, sim_window.index)
                del po_receipt_period

            final_stock = sim_window.closing_stock

            sim_window.previous_backlog =  previous_backlog(sim_window.backlog,sim_window.closing_stock, sim_window.previous_backlog)

            sold = units_sold(sim_window.backlog, sim_window.opening_stock,
                                          sim_window.purchase_order_receipt_qty, sim_window.demand)
            sim_window.sold = sold
            sim_window.revenue = revenue(sku.unit_cost, sold)
            yield sim_window

            del sim_window

            period += 1
        index_item += 1
