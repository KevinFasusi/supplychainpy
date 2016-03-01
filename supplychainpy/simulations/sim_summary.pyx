
def closing_stockout_percentage(closing_stock, period_length):
    cdef float closing_stock_count
    cdef float percentage

    closing_stock_count = closing_stock.count(0)
    percentage = closing_stock_count / period_length
    return percentage

def summarize_monte_carlo(simulation_frame, period_length):

    closing_stock = []
    summarize = []

    for x in range(1, len(simulation_frame)):
        for f in simulation_frame:
            if int(f[0]['index']) == x:
                closing_stock.append(int(f[0]['closing_stock']))
            if len(closing_stock) == period_length:
                cls = closing_stockout_percentage(closing_stock, period_length)
                summarize.append({'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'index': f[0]['index']})
                closing_stock = []
    return summarize

