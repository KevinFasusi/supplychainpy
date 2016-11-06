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
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.bi._recommendation_state_machine import SkuMachine, ProfileMachine
from supplychainpy.bi._recommendations import SKUStates, ProfileStates
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.sample_data.config import ABS_FILE_PATH, FORECAST_PICKLE


def run_sku_recommendation(analysed_orders:UncertainDemand, forecast: dict)->dict:
    """ Runs SKU recommendation state machine and generates recommendations for each sku.

    Args:
        analysed_orders (UncertainDemand):  Analysed Orders.
        forecast (dict):                    forecast.

    Returns:
        dict:   Recommendations for each sku.

    """
    recommend = SkuMachine()
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


def run_profile_recommendation(analysed_orders: UncertainDemand, forecast: dict)->dict:
    """ Runs profile recommendation state machine and generates recommendations for entire inventory profile.

    Args:
        analysed_orders (UncertainDemand):  Analysed orders as UncertainDemand object
        forecast (dict):                    Forecast results for same data set.

    Returns:
        dict:    Recommendations for entire inventory profile

    """
    recommend = ProfileMachine()
    states = ProfileStates(analysed_orders=analysed_orders, forecast=forecast)
    recommend.add_state("start", states.initialise_machine)
    recommend.add_state("revenue", states.revenue)
    recommend.add_state("excess", states.excess)
    recommend.add_state("shortage", states.shortage)
    recommend.add_state("classification", states.classification)
    recommend.add_state("inventory", states.inventory_turns)
    recommend.add_state("recommendation", recommend, end_state=1)
    recommend.set_start("start")
    recommend.run()
    # have to serialise the profile recommendation seperately from the sku recommendation
    return deserialise_config(ABS_FILE_PATH['PROFILE_PICKLE'])


if __name__ == '__main__':
    orders_analysis = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                              z_value=Decimal(1.28),
                                              reorder_cost=Decimal(5000),
                                              file_type="csv",
                                              length=12)

    # d = ProfileGenerator(analysed_orders=orders_analysis)
    # d.Top_Concerns()
    # resp = {}
    #for i in run_sku_recommendation(analysed_orders=orders_analysis, forecast=deserialise_config(FORECAST_PICKLE)).values():
    #   print(i)
    # d = ProfileStates(analysed_orders=orders_analysis, forecast=deserialise_config(FORECAST_PICKLE))
    # d.revenue()
    for i in run_profile_recommendation(analysed_orders=orders_analysis,
                                        forecast=deserialise_config(FORECAST_PICKLE)).values():
        print(i)
