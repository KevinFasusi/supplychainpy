import time
from decimal import Decimal


class AnalyseOrdersSummary:
    __abc = ""

    def __init__(self, abc_xyz):
        self.__abc = abc_xyz

    def classification_summary(self):
        ax_count = 0
        ay_count = 0
        az_count = 0
        bx_count = 0
        by_count = 0
        bz_count = 0
        cx_count = 0
        cy_count = 0
        cz_count = 0

        for sku in self.__abc:

            if sku.abcxyz_classification == "AX":
                ax_count += 1
            elif sku.abcxyz_classification == "AY":
                ay_count += 1
            elif sku.abcxyz_classification == "AZ":
                az_count += 1
            elif sku.abcxyz_classification == "BX":
                bx_count += 1
            elif sku.abcxyz_classification == "BY":
                by_count += 1
            elif sku.abcxyz_classification == "BZ":
                bz_count += 1
            elif sku.abcxyz_classification == "CX":
                cx_count += 1
            elif sku.abcxyz_classification == "CY":
                cy_count += 1
            elif sku.abcxyz_classification == "CZ":
                cz_count += 1
            else:
                pass

        classification_matrix = []
        classification_matrix.append({"AX": ax_count})
        classification_matrix.append({"AY": ay_count})
        classification_matrix.append({"AZ": az_count})
        classification_matrix.append({"BX": bx_count})
        classification_matrix.append({"BY": by_count})
        classification_matrix.append({"BZ": bz_count})
        classification_matrix.append({"CX": cx_count})
        classification_matrix.append({"CY": cy_count})
        classification_matrix.append({"CZ": cz_count})

        return classification_matrix

