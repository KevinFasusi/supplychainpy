from _decimal import ROUND_FLOOR
from math import isclose
from operator import itemgetter

import itertools

from decimal import getcontext

def closing_stockout_percentage(closing_stock, int period_length):
    cdef float closing_stock_count
    cdef float percentage

    closing_stock_count = closing_stock.count(0)
    percentage = closing_stock_count / period_length
    return percentage

def average_closing_cost(shortage_cost, int period_length):
    cdef float average_cost
    average_cost = sum(shortage_cost) / period_length
    return average_cost


def summarize_monte_carlo( simulation_frame, int period_length):

    closing_stock = []
    shortage_cost = []
    summary = []
    summarize = []

    cdef float cls
    cdef unsigned int i , n, x
    cdef float revenue
    n = len(simulation_frame)
    i = 1

    for x in range(i, n ):

        for f in simulation_frame:
            if int(f[0]['index']) == x:
                closing_stock.append( int(f[0]['closing_stock']))
                shortage_cost.append(int(f[0]['shortage_cost']))
                revenue += (int(f[0]['revenue']))
            if len(closing_stock) == period_length and len(shortage_cost) == period_length:
                cls = closing_stockout_percentage(closing_stock, period_length)
                shc = average_closing_cost(shortage_cost, period_length)
                #print(summary)
                summary.append({'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'average_shortage_cost': shc, 'revenue': revenue, 'index': f[0]['index']})
                closing_stock.clear()
                shortage_cost.clear()
                cls = 0
                shc = 0
                revenue = 0

    final_summary = summarise_frame(summary)

    return final_summary

def summarise_frame(sim_frame):
    stockout_probability_summary = []
    cdef float stockout_probability
    cdef float stockout_count
    cdef int count_runs
    cdef float shortage_cost_average
    cdef float sh_avg
    cdef float average_stockout
    cdef float total_stockout
    cdef float total_shortage_cost
    cdef float total_revenue
    cdef float revenue


    summary = []
    sim_frame.sort(key = itemgetter('sku_id'))
    list1 = []
    for key, items in itertools.groupby(sim_frame, itemgetter('sku_id')):
        list1.append(list(items))

    probability_list = []
    for item in list1:
        sku_id = item[0]['sku_id']
        count_runs = len(item)

        for j in item:
            #print("stockout percentage {}".format(j['stockout_percentage']))
            total_stockout += j['stockout_percentage']
            total_revenue +=j['revenue']
            #print("total revenue {}".format(total_revenue))
            total_shortage_cost += j['average_shortage_cost']
        #print("total stockout {}".format(total_stockout))
        avg_stockout = total_stockout/count_runs
        #print("average stockout {}".format(avg_stockout))
        average_shortage_cost = total_shortage_cost/count_runs
        revenue = total_revenue/count_runs
        #print("revenue {}".format(revenue))
        summary.append({'sku_id': sku_id, 'average_stockout': '{:0.2f}'.format(avg_stockout*100), 'revenue':revenue,
                        'average_shortage_cost': average_shortage_cost})
        average_stockout = 0
        average_shortage_cost = 0
        revenue =0
        total_stockout = 0
        total_revenue = 0
        avg_stockout = 0

    #        if float(item[0]['stockout_percentage']) > 0.00:
    #            stockout_count += 1
    #    for j in item:
    #        shortage_cost_average += float(j['average_shortage_cost'])
    #
    #
    #    stockout_probability = (stockout_count/count_runs)
    #    print(stockout_count)
    #    sh_avg = (shortage_cost_average/float(count_runs))
    #    probability_list.append({'sku_id':sku_id, 'stockout_probability': stockout_probability, 'average_shortage_cost':'{:.2f}'.format(sh_avg)})
    #    stockout_count = 0
    #    stockout_probability = 0
    #    sh_avg = 0
    #    shortage_cost_average = 0

    return summary

