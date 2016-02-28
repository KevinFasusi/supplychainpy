from decimal import Decimal


class MonteCarloSummary:
    """
    """

    def __init__(self):
        self._opening_stock_average
        self._opening_stock_min
        self._opening_stock_max
        self._opening_stock_final
        self._opening_stock_std
        self._opening_stock_std
        self._closing_stock_average
        self._closing_stock_min
        self._closing_stock_max
        self._closing_stock_final
        self._closing_stock_std
        self._stock_out_probability
        self._negative_stock_probability
        self._stock_out_count

    @property
    def opening_stock_final(self):
        return self._opening_stock_final

    @opening_stock_final.setter
    def opening_stock_final(self, opening_stock_final: Decimal):
        self._opening_stock_final = opening_stock_final

    @property
    def opening_stock_average(self):
        return self._opening_stock_average

    @opening_stock_average.setter
    def opening_stock_average(self, opening_stock_average: Decimal):
        self._opening_stock_average = opening_stock_average

    @property
    def opening_stock_min(self):
        return self._opening_stock_min

    @opening_stock_min.setter
    def opening_stock_min(self, opening_stock_min: Decimal):
        self._opening_stock_min = opening_stock_min

    @property
    def opening_stock_max(self):
        return self._opening_stock_max

    @opening_stock_max.setter
    def opening_stock_max(self, opening_stock_max: Decimal):
        self._opening_stock_max = opening_stock_max

    @property
    def opening_stock_std(self):
        return self._opening_stock_std

    @opening_stock_std.setter
    def opening_stock_std(self, opening_stock_std: Decimal):
        self._opening_stock_std = opening_stock_std

    @property
    def closing_stock_average(self):
        return self._closing_stock_average

    @closing_stock_average.setter
    def closing_stock_average(self, closing_stock_average: Decimal):
        self._closing_stock_average = closing_stock_average

    @property
    def closing_stock_min(self):
        return self._closing_stock_min

    @closing_stock_min.setter
    def closing_stock_min(self, closing_stock_min: Decimal):
        self._closing_stock_min = closing_stock_min

    @property
    def closing_stock_max(self):
        return self._closing_stock_max

    @closing_stock_max.setter
    def closing_stock_max(self, closing_stock_max: Decimal):
        self._closing_stock_max = closing_stock_max

    @property
    def closing_stock_std(self):
        return self._closing_stock_std

    @closing_stock_std.setter
    def closing_stock_std(self, closing_stock_std: Decimal):
        self._closing_stock_std = closing_stock_std

    @property
    def closing_stock_final(self):
        return self._closing_stock_final

    @closing_stock_final.setter
    def closing_stock_final(self, closing_stock_final: Decimal):
        self._closing_stock_final = closing_stock_final

