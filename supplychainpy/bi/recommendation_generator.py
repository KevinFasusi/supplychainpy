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
from supplychainpy._helpers._pickle_config import serialise_config, deserialise_config
from supplychainpy.bi.recommendation_state_machine import RecommendationStateMachine
from supplychainpy.bi.recommendations import SKUStates
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.sample_data.config import ABS_FILE_PATH, FORECAST_PICKLE, RECOMMENDATION_PICKLE


class Response:
    _compiled_responses = {}  # global attribute dictionary remember to use single under score not double

    def __init__(self):
        self.__dict__ = self._compiled_responses

    @property
    def compile_response(self):
        return self._compiled_responses

    @compile_response.setter
    def compile_response(self, **kwargs):
        self._compiled_responses.update(kwargs)


class ProfileGenerator:
    def __init__(self, analysed_orders: UncertainDemand):
        self.__analysed_orders = analysed_orders
        self.summarised_inventory = Inventory(analysed_orders)

        # self.__forecasts = forecasts # add forecast to object to use for further analysis compare the forecst to
        # quantity on hand and average orders for sku's in shortage

    def Top_Concerns(self):
        total_revenue_all_skus = 0
        for i in self.__analysed_orders:
            total_revenue_all_skus += i.revenue

        top_10_revenue = [item for item in self.summarised_inventory.rank_summary(attribute='revenue',
                                                                                  count=10, reverse=True)]

        revenue_skus = [i.get('sku') for i in top_10_revenue]

        total_revenue = sum([Decimal(description.get('revenue')) for description in
                             self.summarised_inventory.describe_sku(*revenue_skus)])

        top_10_excess = [item for item in self.summarised_inventory.rank_summary(attribute='excess_stock',
                                                                                 count=10, reverse=True)]
        excess_skus = [i.get('sku') for i in top_10_excess]
        total_excess_cost = sum([Decimal(description.get('excess_cost')) for description in
                                 self.summarised_inventory.describe_sku(*excess_skus)])
        sku_inventory_turns = {excess_skus[index]: description.get('inventory_turns') for index, description in
                               enumerate(self.summarised_inventory.describe_sku(*excess_skus))}
        KR202_223 = [description for description in
                     self.summarised_inventory.describe_sku('KR202-223')]
        #print(KR202_223, sku_inventory_turns)
        excess_response = 'Focus on reducing the excess for the following {sku}. These SKU account for {cost} of excess cost. \n'.format(
            **{'sku': excess_skus}, **{'cost': total_excess_cost})

        top_10_shortage = [item for item in self.summarised_inventory.rank_summary(attribute='shortages',
                                                                                   count=10, reverse=True)]

        shortage_skus = [i.get('sku') for i in top_10_shortage]

        total_shortages = sum([Decimal(description.get('shortage_cost')) for description in
                               self.summarised_inventory.describe_sku(*shortage_skus)])

        shortage_skus_top_revenue = [i.get('sku') for i in top_10_shortage if i.get('sku') in revenue_skus]

        shortage_skus_top_revenue_total = sum([Decimal(description.get('revenue')) for description in
                                               self.summarised_inventory.describe_sku(*revenue_skus)])

        shortage_response = 'Consider increasing the stock holding of the following SKU: {sku}. ' \
                            'The total cost of covering the shortages is {cost}. ' \
                            'Give more consideration to SKUs {rev_sku} as they are particularly important, ' \
                            'they are in the top 10 contributors to yearly revenue, they contribute {contr_rev:.2f} which is {perc: .2f}% ' \
                            'of total revenue.'.format(
            **{'sku': shortage_skus}, **{'cost': total_shortages},
            **{'rev_sku': shortage_skus_top_revenue},
            **{'contr_rev': shortage_skus_top_revenue_total},
            **{'perc': (shortage_skus_top_revenue_total / total_revenue_all_skus) * 100}

        )

        print('{}{} For more information please view the details for each sku in the SKU view.'.format(excess_response,
                                                                                                       shortage_response))


def run_sku_recommendation_state_machine(analysed_orders, forecast):

    recommend = RecommendationStateMachine()
    states = SKUStates(analysed_orders=analysed_orders, forecast=forecast)
    recommend.add_state("start", states.initialise_machine)
    recommend.add_state("excess_rank", states.excess_rank)
    recommend.add_state("shortage_rank", states.shortage_rank)
    recommend.add_state("inventory_turns", states.inventory_turns)
    recommend.add_state("classification", states.classification)
    recommend.add_state("traffic_light", states.traffic_light)
    recommend.add_state("forecast", states.forecast)
    recommend.add_state("recommendation", recommend, end_state=1)
    recommend.set_start("start")
    for sku in analysed_orders:
        recommend.run(sku.sku_id)
    return deserialise_config(ABS_FILE_PATH['RECOMMENDATION_PICKLE'])


def run_profile_recommendation_state_machine(analysed_orders, forecast):
    pass



if __name__ == '__main__':
    orders_analysis = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                              z_value=Decimal(1.28),
                                              reorder_cost=Decimal(5000),
                                              file_type="csv",
                                              length=12)

    d = ProfileGenerator(analysed_orders=orders_analysis)
    d.Top_Concerns()
    resp = {}
   # for i in run_sku_recommendation_state_machine(analysed_orders=orders_analysis, forecast=deserialise_config(FORECAST_PICKLE)).values():
    #   print(i)
