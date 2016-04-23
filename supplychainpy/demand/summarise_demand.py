import time
from decimal import Decimal


class AnalyseOrdersSummary:
    __abc = ""

    def __init__(self, abc_xyz):
        self.__abc = abc_xyz

    def classification_summary(self):
        ax_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'AX']

        ay_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'AY']

        az_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'AZ']

        bx_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'BX']

        by_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'BY']

        bz_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'BZ']

        cx_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'CX']

        cy_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'CY']

        cz_count = [sku for sku in self.__abc if sku.abcxyz_classification == 'CZ']

        classification_matrix = {}
        classification_matrix.update({"AX": ax_count.__len__()})
        classification_matrix.update({"AY": ay_count.__len__()})
        classification_matrix.update({"AZ": az_count.__len__()})
        classification_matrix.update({"BX": bx_count.__len__()})
        classification_matrix.update({"BY": by_count.__len__()})
        classification_matrix.update({"BZ": bz_count.__len__()})
        classification_matrix.update({"CX": cx_count.__len__()})
        classification_matrix.update({"CY": cy_count.__len__()})
        classification_matrix.update({"CZ": cz_count.__len__()})

        return classification_matrix
