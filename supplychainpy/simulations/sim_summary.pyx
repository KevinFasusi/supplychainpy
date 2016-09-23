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

from operator import itemgetter

import itertools

def closing_stockout_percentage( list closing_stock, int period_length):

    cdef float closing_stock_count
    cdef float percentage

    closing_stock_count = closing_stock.count(0)
    percentage = closing_stock_count / period_length
    return percentage

def average_items(shortage_cost, int period_length):
    cdef float average
    average = sum(shortage_cost) / period_length
    return average


def optimum_std(float mean, list items):
    cdef list diff =[]
    cdef double variance, std, tmp
    cdef dict variance_analysis ={}

    for item in items:
        tmp = (item - mean)**2
        diff.append(tmp)

    variance = sum(diff)/len(diff)
    std = variance ** 0.5
    variance_analysis = {'variance': variance, 'standard_deviation': std}

    return variance_analysis


def summarize_monte_carlo(list simulation_frame, int period_length):
    """ summarises the monte carlo transaction summary

    Generates random distribution for demand over period specified and creates a simulation window for opening_stock,
    demand, closing_stock, delivery and backlog for each sku in the data set. Creates a transaction summary window
    for inventory movements.

    Args:
        simulation_frame (list):    The path to the file containing two columns of data, 1 period and 1 data-point per sku.
        period_length (int):        The number of periods define the simulation window e.g. 12 weeks, months etc.


    Returns:
        list:       A list containing the transaction summary for each period.

    """

    cdef:
        list closing_stock = [], opening_stock =[], shortage_units = [], summary = []
        list summarize = [], quantity_sold =[], backlog =[]

    cdef unsigned int i , n, x

    cdef:
        float cls, avg_ops, min_ops, max_ops, avg_backlog, min_backlog, max_backlog
        float avg_cls, min_cls, max_cls
        double shc, min_shc, max_shc, rev, min_quantity_sold, max_quantity_sold, var_ops, avg_shc, total_quantity_sold

    cdef dict std_ops ={}, std_backlog={}, std_cls={}, std_shc={}, std_quantity_sold={}


    n = len(simulation_frame)

    i = 1

    for x in range(i, n ):

        for f in simulation_frame:
            if int(f[0]['index']) == x:
                closing_stock.append( int(f[0]['closing_stock']))
                shortage_units.append(float(f[0]['shortage_units']))
                quantity_sold.append(int(f[0]['quantity_sold']))
                opening_stock.append(int(f[0]['opening_stock']))
                backlog.append(int(f[0]['backlog']))

            if len(closing_stock) == period_length and len(shortage_units) == period_length:
                cls = closing_stockout_percentage(closing_stock, period_length)
                avg_ops = average_items(opening_stock, period_length)
                min_ops = min(opening_stock)
                max_ops = max(opening_stock)
                std_ops = optimum_std(avg_ops, opening_stock)
                avg_backlog = average_items(backlog, period_length)
                min_backlog = min(backlog)
                max_backlog = max(backlog)
                std_backlog = optimum_std(avg_backlog, backlog)
                avg_cls = average_items(closing_stock, period_length)
                min_cls = min(closing_stock)
                max_cls = max(closing_stock)
                std_cls = optimum_std(avg_cls, closing_stock)
                shc = sum(shortage_units)
                min_shc = min(shortage_units)
                max_shc = max(shortage_units)
                avg_shc = average_items(shortage_units, period_length)
                std_shc = optimum_std(avg_shc, shortage_units)
                total_quantity_sold = sum(quantity_sold)
                avg_qty_sold = average_items(quantity_sold, period_length)
                min_quantity_sold = min(quantity_sold)
                max_quantity_sold = max(quantity_sold)
                std_quantity_sold = optimum_std(avg_qty_sold, quantity_sold)

                summary.append({'sku_id': f[0]['sku_id'],
                                'standard_deviation_opening_stock': std_ops['standard_deviation'],
                                'variance_opening_stock': std_ops['variance'],
                                'stockout_percentage': cls,
                                'average_closing_stock': avg_cls,
                                'minimum_closing_stock': min_cls,
                                'maximum_closing_stock': max_cls ,
                                'standard_deviation_closing_stock': std_cls['standard_deviation'],
                                'variance_closing_stock': std_cls['variance'],
                                'total_shortage_units': shc,
                                'standard_deviation_shortage_cost': std_shc['standard_deviation'],
                                'variance_shortage_units': std_shc['variance'],
                                'standard_deviation_revenue': std_quantity_sold['standard_deviation'],
                                'variance_quantity_sold': std_quantity_sold['variance'],
                                'minimum_shortage_units':min_shc,
                                'maximum_shortage_units': max_shc,
                                'average_opening_stock': avg_ops,
                                'minimum_opening_stock': min_ops,
                                'maximum_opening_stock': max_ops,
                                'average_quantity_sold': avg_qty_sold,
                                'minimum_quantity_sold': min_quantity_sold,
                                'maximum_quantity_sold': max_quantity_sold,
                                'average_backlog': avg_backlog,
                                'minimum_backlog': min_backlog,
                                'maximum_backlog': max_backlog,
                                'standard_deviation_backlog': std_backlog['standard_deviation'],
                                'variance_backlog': std_backlog['variance'],
                                'index': f[0]['index']}
                               )

                closing_stock.clear()
                shortage_units.clear()
                quantity_sold.clear()
                opening_stock.clear()
                backlog.clear()


    # allow interface to retrieve this level of analysis and then option to summarise the frame

    return summary

def frame(sim_frame):

    cdef int count_runs
    cdef double  revenue, avg_quantity_sold
    cdef:
        list summary=[], item_list=[], min_closing_stock=[], max_closing_stock=[], variance_closing_stock=[],
        average_backlog=[], total_stockout=[]

    cdef list total_revenue=[]
    cdef list max_quantity_sold=[]
    cdef list min_quantity_sold=[]
    cdef list variance_quantity_sold=[]
    cdef list min_opening_stock=[]
    cdef list average_closing_stock=[]

    cdef:
        list max_opening_stock=[], variance_opening_stock=[], min_backlog=[], max_backlog=[], variance_backlog=[],
        average_opening_stock=[], total_shortage_units =[], average_quantity_sold=[]

    cdef unsigned int min_cls, max_cls ,min_opn, max_opn
    cdef double avg_variance_opn, min_bklg, max_bklg, avg_bklg, avg_variance_bklg, std_bklg, avg_variance_cls, std_cls,\
        avg_cls, std_opn, max_qs, min_qs
    cdef float std_quantity_sold, avg_stockout


    sim_frame.sort(key = itemgetter('sku_id'))

    for key, items in itertools.groupby(sim_frame, itemgetter('sku_id')):
        item_list.append(list(items))

    for item in item_list:
        sku_id = item[0]['sku_id']
        count_runs = len(item)


        for j in item:
            total_stockout.append(j['stockout_percentage'])
            average_quantity_sold.append(j['average_quantity_sold'])
            total_shortage_units.append(j['total_shortage_units'])
            min_closing_stock.append(j['minimum_closing_stock'])
            max_closing_stock.append(j['maximum_closing_stock'])
            variance_closing_stock.append(j['variance_closing_stock'])
            min_opening_stock.append(j['minimum_opening_stock'])
            max_opening_stock.append(j['maximum_opening_stock'])
            variance_opening_stock.append(j['variance_opening_stock'])
            min_backlog.append(j['minimum_backlog'])
            max_backlog.append(j['maximum_backlog'])
            variance_backlog.append(j['variance_backlog'])
            max_quantity_sold.append(j['maximum_quantity_sold'])
            min_quantity_sold.append(j['minimum_quantity_sold'])
            variance_quantity_sold.append(j['variance_quantity_sold'])
            average_closing_stock.append(j['average_closing_stock'])
            average_backlog.append(j['average_backlog'])



        min_cls = min(min_closing_stock)
        max_cls = max(max_closing_stock)
        avg_cls = average_items(average_closing_stock, count_runs)
        avg_variance_cls =  average_items(variance_closing_stock, count_runs)
        std_cls = avg_variance_cls ** 0.5
        min_opn = min(min_opening_stock)
        max_opn = max(max_opening_stock)
        avg_variance_opn = average_items(variance_opening_stock, count_runs)
        std_opn = avg_variance_opn ** 0.5
        max_qs = max(max_quantity_sold)
        min_qs = min(min_quantity_sold)
        min_bklg = min(min_backlog)
        max_bklg = max(max_backlog)
        avg_variance_bklg = average_items(variance_backlog, count_runs)
        std_bklg = avg_variance_bklg ** 0.5
        avg_bklg = average_items(average_backlog, count_runs)
        avg_variance = average_items(variance_quantity_sold, count_runs)
        avg_quantity_sold = average_items(average_quantity_sold, count_runs)
        std_quantity_sold = avg_variance ** 0.5
        avg_stockout = average_items(total_stockout, count_runs)
        average_shortage_units = average_items(total_shortage_units, count_runs)
        summary.append({'sku_id': sku_id,
                        'minimum_closing_stock': min_cls,
                        'maximum_closing_stock': max_cls,
                        'average_closing_stock': "{:.0f}".format(avg_cls),
                        'standard_deviation_closing_stock': "{:.0f}".format(std_cls),
                        'service_level': '{:0.2f}'.format((1-avg_stockout)*100),
                        'average_quantity_sold': "{:.0f}".format(avg_quantity_sold),
                        'maximum_quantity_sold': max_qs,
                        'minimum_quantity_sold': min_qs,
                        'minimum_backlog': min_bklg,
                        'maximum_backlog': max_bklg,
                        'average_backlog': "{:.0f}".format(avg_bklg),
                        'standard_deviation_backlog': "{:.0f}".format(std_bklg),
                        'minimum_opening_stock': min_opn,
                        'maximum_opening_stock': max_opn,
                        'variance_opening_stock': "{:.0f}".format(std_opn),
                        'standard_deviation_quantity_sold':"{:.0f}".format(std_quantity_sold),
                        'average_shortage_units': "{:.0f}".format(average_shortage_units)})

        min_closing_stock.clear()
        max_closing_stock.clear()
        min_backlog.clear()
        max_backlog.clear()
        average_backlog.clear()
        min_opening_stock.clear()
        max_opening_stock.clear()
        average_opening_stock.clear()
        max_quantity_sold.clear()
        min_quantity_sold.clear()
        variance_quantity_sold.clear()
        total_revenue.clear()
        variance_closing_stock.clear()
        variance_opening_stock.clear()
        variance_backlog.clear()
        variance_quantity_sold.clear()
        average_closing_stock.clear()
        average_quantity_sold.clear()
        total_shortage_units.clear()
        total_stockout.clear()


        average_shortage_cost = 0
        revenue =0
        avg_stockout = 0

    return summary


def optimise_sim(list orders_analysis , list frame_summary, float service_level):

    cdef float f
    return f


def optimise_service_level(list frame_summary, list orders_analysis, double service_level, int runs,
                           double percentage_increase):
    """ Optimises the safety stock for declared service level.

    Identifies which skus under performed (experiencing a service level lower than expected) after simulating
    transactions over a specific period. The safety stock for these items are increased and the analysis is monte carlo
    is run again.


    Args:
        frame_summary (list):           window summary for each period multiplied by the number of runs.
        orders_analysis (list):         prior analysis of orders data.
        service_level (double):           required service level as a percentage.
        runs (int):                     number of runs from previous
        percentage_increase (double):    the percentage increase required

    Returns:
       list:    Updated orders analysis with new saftey stock values based optimised from the simulation. The initial values
                from the analytical model.

    """
    # compare service levels, build list of skus below service level, change their safety stock increase by a percentage
    # run the monte carlo, keep doing until all skus' are above the requested service level
    # sim_optimise = optimise_sim(service_level=service_level, frame_summary=frame_summary, orders_analysis=orders_analysis)

    count_skus = True

    while count_skus:
        count_skus = False
        for sku in orders_analysis:
            for item in frame_summary:
                if sku.sku_id == item['sku_id']:
                    if float(item['service_level']) <= service_level:
                        count_skus = True
                        sku.safety_stock = round(float(sku.safety_stock)) * percentage_increase
                        break

#       sim = run_monte_carlo(orders_analysis=orders_analysis, runs=runs, period_length=12)

#       sim_window = summarize_window(simulation_frame=sim, period_length=12)

##       sim_frame = summarise_frame(sim_window)

    return orders_analysis
