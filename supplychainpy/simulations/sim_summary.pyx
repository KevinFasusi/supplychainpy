from operator import itemgetter

import itertools

def closing_stockout_percentage( closing_stock, int period_length):
    cdef float closing_stock_count
    cdef float percentage

    closing_stock_count = closing_stock.count(0)
    percentage = closing_stock_count / period_length
    return percentage


def summarize_probability(stockouts):
    cdef int count
    cdef float probability

    if len(stockouts) == 0:
        probability = 0
    else:
        counts = stockouts.count(0)
        probability = len(stockouts) / 1


    return probability


def summarize_monte_carlo( simulation_frame, int period_length):

    closing_stock = []
    summary = []
    summarize = []
    cdef float cls
    cdef unsigned int i , n, x

    n = len(simulation_frame)
    i = 1

    for x in range(i, n ):
        for f in simulation_frame:
            if int(f[0]['index']) == x:
                closing_stock.append( int(f[0]['closing_stock']))
            if len(closing_stock) == period_length:
                cls = closing_stockout_percentage(closing_stock, period_length)
                summary.append({'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'index': f[0]['index']})
                closing_stock = []


    stockout_probability_summary = []
    cdef float stockout_probability
    cdef float stockout_count
    cdef int count_runs

    summary.sort(key = itemgetter('sku_id'))
    list1 = []
    for key, items in itertools.groupby(summary, itemgetter('sku_id')):
        list1.append(list(items))

    probability_list = []
    for item in list1:
        sku_id = item[0]['sku_id']
        count_runs = len(item)
        for j in range(count_runs):
            if float(item[0]['stockout_percentage']) > 0:
                stockout_count += 1
        stockout_probability = (stockout_count/float(count_runs)) * 100
        probability_list.append((sku_id, stockout_probability))
        stockout_count = 0

    return probability_list

