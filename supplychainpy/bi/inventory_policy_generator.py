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

from decimal import Decimal
from supplychainpy import model_inventory
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.sample_data.config import ABS_FILE_PATH


class InventoryProfilePolicyGenerator:
    def __init__(self, analysed_orders: UncertainDemand, forecasts: dict):
        self.__analysed_orders = analysed_orders
        self.__summarised_inventory = Inventory(analysed_orders)
        self.__forecasts = forecasts # add forecast to object to use for further analysis compare the forecst to
        # quantity on hand and average orders for sku's in shortage

    def Top_Concerns(self):
        total_revenue_all_skus = 0
        for i in self.__analysed_orders:
            total_revenue_all_skus += i.revenue

        top_10_revenue = [item for item in self.__summarised_inventory.rank_summary(attribute='revenue',
                                                                                    count=10, reverse=True)]

        revenue_skus = [i.get('sku') for i in top_10_revenue]

        total_revenue = sum([Decimal(description.get('revenue')) for description in
                             self.__summarised_inventory.describe_sku(*revenue_skus)])

        top_10_excess = [item for item in self.__summarised_inventory.rank_summary(attribute='excess_stock',
                                                                                   count=10, reverse=True)]
        excess_skus = [i.get('sku') for i in top_10_excess]
        total_excess_cost = sum([Decimal(description.get('excess_cost')) for description in
                                 self.__summarised_inventory.describe_sku(*excess_skus)])

        excess_response = 'Focus on reducing the excess for the following {sku}. These SKU account for {cost} of excess cost. \n'.format(
            **{'sku': excess_skus}, **{'cost': total_excess_cost})

        top_10_shortage = [item for item in self.__summarised_inventory.rank_summary(attribute='shortages',
                                                                                     count=10, reverse=True)]

        shortage_skus = [i.get('sku') for i in top_10_shortage]

        total_shortages = sum([Decimal(description.get('shortage_cost')) for description in
                               self.__summarised_inventory.describe_sku(*shortage_skus)])

        shortage_skus_top_revenue = [i.get('sku') for i in top_10_shortage if i.get('sku') in revenue_skus]

        shortage_skus_top_revenue_total = sum([Decimal(description.get('revenue')) for description in
                                               self.__summarised_inventory.describe_sku(*revenue_skus)])

        shortage_response = 'Consider increasing the stock holding of the following SKU: {sku}. ' \
                            'The total cost of covering the shortages is {cost}. ' \
                            'Give more consideration to SKUs {rev_sku} as they are particulary important, ' \
                            'they are in the top 10 contributors to yearly revenue, they contribute {contr_rev:.2f} which is {perc: .2f}% ' \
                            'of total revenue.'.format(
            **{'sku': shortage_skus}, **{'cost': total_shortages},
            **{'rev_sku': shortage_skus_top_revenue},
            **{'contr_rev': shortage_skus_top_revenue_total},
            **{'perc': (shortage_skus_top_revenue_total/ total_revenue_all_skus)* 100}

        )

        print('{}{} For more information please view the details for each sku in the SKU view.'.format(excess_response, shortage_response))


class SKUPolicyGenerator(InventoryProfilePolicyGenerator):
    def __init__(self, analysed_orders: UncertainDemand):
        super().__init__(analysed_orders=analysed_orders)


if __name__ == '__main__':
    orders_analysis = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                              z_value=Decimal(1.28),
                                              reorder_cost=Decimal(5000),
                                              file_type="csv",
                                              length=12)

    d = InventoryProfilePolicyGenerator(analysed_orders=orders_analysis)
    d.Top_Concerns()
