class MonteCarloFrameSummary:
    def __init__(self):
        pass

    @staticmethod
    def closing_stockout_percentage(closing_stock: list, period_length: int):
        """ Calculates the percentage of stock out that occurred during the period specified.


        Args:
            period_length (int):    length of window e.g. 12 weeks for a quarter etc.
            closing_stock (list):   list of closing stock values for a given sku over the same time frame
                                    as the period_length


        Returns:
            float:   Percentage of final closing stock values that result in stock out and backlog.

        Raises:
            ValueError: The number of stock positions and the period length must match exactly.
        """
        if len(closing_stock) != period_length:
            raise ValueError(" The number of stock positions and the period length must match exactly.\nThe"
                             " number of stock positions passed for closing stock is currently {}. "
                             "The length specified for period_length is currently {}".format(len(closing_stock),
                                                                                                 period_length))

        closing_stock_count = ([x for x in closing_stock if x <= 0])
        percentage = len(closing_stock_count) / period_length
        return percentage
