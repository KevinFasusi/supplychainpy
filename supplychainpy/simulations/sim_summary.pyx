from operator import itemgetter

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
                summary.append([{'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'index': f[0]['index']}])
                closing_stock = []


    stockout_probability_summary = []
    probability =0
    count = 0

    for s in sorted(summary,key=itemgetter('sku_id')):
        if float(s[0]['stockout_percentage']) == 0.0:
            probability += 1
            count +=1


            print(probability)
       # if  len(probability) == len(gr):
       #     summarized_probability = summarize_probability(probability)
       #     probability_summary = {gr[0]['sku_id']: summarized_probability}
       #     stockout_probability_summary.append(probability_summary)

    return stockout_probability_summary


