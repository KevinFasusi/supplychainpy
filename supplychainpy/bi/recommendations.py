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
import heapq
from copy import deepcopy
from decimal import Decimal

from supplychainpy._helpers._codes import Currency
from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.sample_data.config import ABS_FILE_PATH


class ResponseBorg:
    """ Borg class making  class attributes global """

    _shared_response = {}  # global attribute dictionary

    def __init__(self):
        self.__dict__ = self._shared_response


class ResponseSingleton(ResponseBorg):
    """ Singleton class using global dict in ResponseBorg"""

    def __init__(self, **kwargs):
        ResponseBorg.__init__(self)
        self._shared_response.update(kwargs)

    @property
    def shared_response(self) -> dict:
        return self._shared_response

    def __str__(self):
        # returns the attribute for printing
        return str(self._shared_response)


class SKUStates:
    """Contains states required to generate recommendations for individual SKUs"""
    _END_STATE = 'recommendation'
    _EMPTY = 'EMPTY'
    _TRANSITION_STATES = {
        'EXCESS_RANK_STATE': 'excess_rank',
        'SHORTAGE_RANK_STATE': 'shortage_rank',
        'INVENTORY_TURNS_STATE': 'inventory_turns',
        'CLASSIFICATION_STATE': 'classification',
        'TRAFFIC_LIGHT_STATE': 'traffic_light',
        'FORECAST_STATE': 'forecast',
        'RECOMMENDATION_STATE': 'recommendation'
    }

    def __init__(self, analysed_orders: UncertainDemand, forecast: dict = None):
        self._analysed_orders = analysed_orders
        self._summarised_inventory = Inventory(analysed_orders)
        self._htces_forecast = forecast
        self._summary = {}
        self._compiled_response = ResponseSingleton()
        self._currency_symbol = self._retrieve_currency()

    @property
    def currency(self):
        return self._currency_symbol

    @property
    def analysed_orders(self) -> UncertainDemand:
        return self._analysed_orders

    @property
    def summarised_inventory(self) -> Inventory:
        return self._summarised_inventory

    @property
    def htces_forecast(self) -> dict:
        return self._htces_forecast

    @property
    def compiled_response(self) -> ResponseSingleton:
        return self._compiled_response

    @property
    def summary(self) -> dict:
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    def _retrieve_currency(self) -> str:
        currency_code = ''
        for i in self.analysed_orders:
            currency_code = i.currency
            break
        symbol = Currency(code=currency_code)
        return symbol.retrieve_symbol()

    def _setup_summary(self, sku: str):
        """Prepares summary for each sku.

        Args:
            sku (str):  SKU unique identification

        """
        self.summary = [description for description in
                        self._summarised_inventory.describe_sku(sku)][0]

    def initialise_machine(self, sku: str) -> tuple:
        """Initialises state machine.

        Args:
            sku (str): SKU unique identification

        Returns:
            tuple:  New State and sku unique identification

        """
        self._setup_summary(sku=sku)
        excess_units = int(self._summary.get('excess_units'))
        shortage_units = int(self._summary.get('shortage_units'))
        if excess_units > 0:
            state = self._TRANSITION_STATES.get('EXCESS_RANK_STATE', self._END_STATE)
        elif shortage_units > 0:
            state = self._TRANSITION_STATES.get('SHORTAGE_RANK_STATE', self._END_STATE)
        else:
            state = self._TRANSITION_STATES.get('INVENTORY_TURNS_STATE', self._END_STATE)
        return state, sku

    def append_response(self, response: str, sku: str):
        """ Appends each response to the dict in the singleton.

        Args:
            response:
            sku:

        Returns:

        """

        resp = self.compiled_response.shared_response.get(sku, self._EMPTY)
        if self._EMPTY != resp:
            response = resp + response
            self.compiled_response.shared_response.update(**{'{}'.format(sku): response})
        else:
            self.compiled_response.shared_response.update(**{'{}'.format(sku): response})

    def excess_rank(self, sku: str) -> tuple:
        """Excess State.

        Args:
            sku (str):    SKU unique identification number.

        Returns:
            str:    New state and SKU ID

        """
        excess_rank = int(self._summary.get('excess_rank', 11))

        if excess_rank <= 10:
            response = '{} is one of the top 10 overstocked SKUs in your inventory profile, ranked {} of ' \
                       '10 overstocked SKUs. '.format(sku, sku, excess_rank)

            self.append_response(response=response, sku=sku)
            sku_classification = self._summary.get('classification', 'XX')
            if sku_classification == 'AX':
                quantity_on_hand = self._summary.get('quantity_on_hand')
                reorder_quantity = self._summary.get('reorder_quantity')
                response = 'The {} inventory classification indicates a stable demand profile. ' \
                           'SKU {} is in the 20% of SKU\'s that contribute 80% yearly revenue. ' \
                           'Unless {} product is approaching end of life (EOL)' \
                           ', there is likely little need to panic. ' \
                           'Holding purchase orders for this SKU will reduce ' \
                           'the excess. Review consumption of this SKU until the quantity on hand, ' \
                           'currently {}, is close to or below the reorder level of {}. '.format(sku_classification,
                                                                                                 sku, sku,
                                                                                                 quantity_on_hand,
                                                                                                 reorder_quantity)
                self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('INVENTORY_TURNS_STATE', self._END_STATE)
        return state, sku

    def shortage_rank(self, sku: str) -> tuple:
        """Shortage rank state

        Args:
            sku (str):    SKU unique identification.

        Returns:
            tuple:        New state and SKU ID

        """
        shortage_rank = int(self._summary.get('shortage_rank', 11))
        if shortage_rank <= 10:
            response = '{} is one of the top 10 understocked SKUs ' \
                       'in your inventory profile. {} is currently ranked {} of ' \
                       '10 understocked SKUs. '.format(sku, sku, shortage_rank)
            self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('INVENTORY_TURNS_STATE', self._END_STATE)
        return state, sku

    def inventory_turns(self, sku: str) -> tuple:
        """Inventory turns state.

        Args:
            sku:    SKU unique identification.

        Returns:
            tuple:  New state and SKU ID

        """
        inventory_turns = float(self._summary.get('inventory_turns'))
        excess_rank = int(self._summary.get('excess_rank', 11))
        if inventory_turns <= 2.00 and excess_rank <= 10:
            response = '{} has a very low rolling inventory turn rate at {:.2f}. {} may be a greater cause for ' \
                       'concern considering it is also in the top 10 overstocked ' \
                       'SKUs in the inventory profile. '.format(sku, float(self._summary.get('inventory_turns')), sku)

            self.append_response(response=response, sku=sku)
        elif inventory_turns <= 2.00:
            response = '{} has a very low rolling inventory turn rate at {:.2f}. '.format(
                sku, float(self._summary.get('inventory_turns')))
            self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('CLASSIFICATION_STATE', self._END_STATE)
        return state, sku

    def classification(self, sku: str) -> tuple:
        """Classification state.

        Args:
            sku (str):    SKU ID number

        Returns:
           tuple:     New state and SKU ID

        """

        classification = self._summary.get('classification')
        unit_cost_rank = self._summary.get('unit_cost_rank')
        excess_rank = int(self._summary.get('excess_rank', 11))

        if classification in ('AZ', 'BZ', 'CZ'):
            response = 'The {} classification indicates that {} has volatile demand, ' \
                       'making it difficult to predict' \
                       ' the consumption of the excess. '.format(self._summary.get('classification'), sku)
            self.append_response(response=response, sku=sku)

        if classification == 'CZ' and unit_cost_rank < 10 and excess_rank <= 10:
            response = '{} is a slow moving volatile SKU. A unit cost of {} makes it also one of the more costly' \
                       ' in the inventory profile.  ' \
                       'It may be prudent to make financial provisions for this product, ' \
                       'discount them or bundle them with a complimentary popular product ' \
                       'in a promotion. '.format(sku, self._summary.get('unit_cost'))
            self.append_response(response=response, sku=sku)

        if classification in ('AX', 'BX'):
            response = 'The {} classification, indicates that {} has a stable demand profile and ' \
                       'contributes significantly to revenue. ' \
                       'Corrective action should be taken to bring the quantity on hand (QOH) up from {} to {}. '
            self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('TRAFFIC_LIGHT_STATE', self._END_STATE)
        return state, sku

    def traffic_light(self, sku: str) -> tuple:
        """ Traffic light state.

        Args:
            sku (str):    SKU ID number

        Returns:
            tuple:  New state and SKU ID

        """
        traffic_light = self._summary.get('inventory_traffic_light')
        excess_units = int(self._summary.get('excess_units', 11))
        classification = self._summary.get('classification')
        shortage_units = int(self._summary.get('shortage_units', 11))

        if traffic_light == 'white':
            response = 'The QOH is less than 75% of safety stock, implying a substantial depletion of ' \
                       'buffer stock. Take into consideration that it is acceptable ' \
                       'to dip into safety stock approximately 50% of the time. However, this situation ' \
                       'poses a threat for servicing future demand. This situation may be acceptable if this product ' \
                       'is \'end of life\' and the goal is to drive down stock. Corrective action is ' \
                       'required if it is not currently a policy to reduce the QOH for {}, and the ' \
                       'receipt of a purchase order is not imminent. '.format(sku)
            self.append_response(response=response, sku=sku)
        elif traffic_light == 'red':
            response = 'The QOH is less 50% of the recommended safety stock. ' \
                       'Take into consideration that it is acceptable ' \
                       'to dip into safety stock approximately 50% of the time, consuming ' \
                       'approximately 50% of its value.' \
                       'Therefore, in this situation there may be little imminent threat to the service level. ' \
                       'Checking that a purchase order has been placed may be prudent. '.format(sku)
            self.append_response(response=response, sku=sku)
        elif traffic_light == 'amber':
            response = 'The QOH is less than the reorder level but has yet to hit safety stock. ' \
                       'There is little to worry about at this point. The periodic review of inventory ' \
                       'and communication of any upcoming deals or promotions ' \
                       'that may significantly impact the demand profile should be a focus.'
            self.append_response(response=response, sku=sku)
        elif traffic_light == 'green' and excess_units == 0 and classification not in ('CZ', 'CY', 'BZ', 'AZ') \
                and shortage_units == 0:

            response = 'Congratulations the QOH is within optimal boundaries.  ' \
                       'There is little to worry about at this point. The periodic review of stock ' \
                       'and communication of any upcoming deals or promotions that may significantly ' \
                       'impact the demand profile should be a focus. '
            self.append_response(response=response, sku=sku)
        state = self._TRANSITION_STATES.get('FORECAST_STATE', self._END_STATE)
        return state, sku

    def forecast(self, sku: str) -> tuple:
        """Forecast state.

        Args:
            sku (str):    SKU unique identification number

        Returns:
            tuple:

        """
        # if the demand shows a linear trend then check if the forecast is less than the excess units.
        if self._htces_forecast.get(sku)['statistics']['trend']:
            if self._htces_forecast.get(sku)['forecast'][0] < int(self._summary.get('excess_units')):
                response = 'It is unlikely {} will fair better next month as the most optimistic forecast is '
                self.append_response(response=response, sku=sku)
        if self._htces_forecast.get(sku)['statistics']['trend'] and int(self._summary.get('excess_units')) > 0 \
                and self._summary.get('classification') in ('AX', 'AY', 'BX', 'BY', 'CX') \
                and self._htces_forecast.get(sku)['forecast'][0] > int(self._summary.get('excess_units')):
            response = 'The current excess can be reduced by reducing purchase orders and allow the ' \
                       'forecasted demand to be catered for from stock. '
            self.append_response(response=response, sku=sku)
        state = self._TRANSITION_STATES.get('RECOMMENDATION_STATE', self._END_STATE)
        serialise_config(configuration=self._compiled_response.shared_response,
                         file_path=ABS_FILE_PATH['RECOMMENDATION_PICKLE'])
        return state, sku


class ProfileStates(SKUStates):
    _TRANSITION_STATES = {
        'EXCESS_STATE': 'excess',
        'SHORTAGE_STATE': 'shortage',
        'CLASSIFICATION_STATE': 'classification',
        'REVENUE_STATE': 'revenue',
        'RECOMMENDATION_STATE': 'recommendation',
        'INVENTORY_STATE': 'inventory'
    }

    def __init__(self, analysed_orders: UncertainDemand, forecast: dict = None):
        super(ProfileStates, self).__init__(analysed_orders=analysed_orders, forecast=forecast)
        self._total_revenue = self._total_revenue()

    def initialise_machine(self, sku: str = None):
        state = self._TRANSITION_STATES.get('REVENUE_STATE', self._END_STATE)
        return state

    @property
    def total_revenue(self):
        return self._total_revenue

    def _total_revenue(self) -> Decimal:
        """ Calculates the value for total revenue.
        Returns:
            Decimal: The total revenue of the skus in the inventory profile.

        """
        total_revenue_all_skus = Decimal(0)
        for i in self.analysed_orders:
            total_revenue_all_skus += i.revenue
        return total_revenue_all_skus

    def append_response(self, response: str, sku: str):
        """ Appends each response to the dict in the singleton.

        Args:
            response (str):    Recommendation for transition state
            sku (str):         SKU unique identification number

        """

        resp = self.compiled_response.shared_response.get("profile", "")
        response = resp + response
        self.compiled_response.shared_response.update(**{'{}'.format("profile"): response})

    def _percentage_of_revenue(self, revenue):
        return (revenue / self.total_revenue) ** 100

    def _rank_summary(self, attribute: str, count: int) -> list:
        """ Summarised rank

        Args:
            attribute (str):    SKU summary attribute to rank.
            count (int):        Number of items to rank.

        Returns:

        """
        return [item for item in self.summarised_inventory.rank_summary(attribute=attribute,
                                                                        count=count, reverse=True)]

    def revenue(self, sku: str = None) -> str:
        """

        Args:
            sku (str):  SKU unique identification.

        Returns:
            str:        New state.

        """
        top_10_revenue = self._rank_summary(attribute='revenue', count=10)
        top_10_revenue_skus = [summary.get('sku') for summary in top_10_revenue]
        top_10_revenue_total = sum([Decimal(summary.get('revenue')) for summary in top_10_revenue])

        response = 'SKUs {SKUs} are the top ten contributors to revenue, generating ' \
                   '{currency_symbol}{revenue:,.2f} of revenue. '.format(**{'SKUs': ", ".join(top_10_revenue_skus)},
                                                                        **{'currency_symbol': self.currency},
                                                                        **{'revenue': top_10_revenue_total}, )

        self.append_response(response=response, sku=sku)
        state = self._TRANSITION_STATES.get('CLASSIFICATION_STATE', self._END_STATE)
        return state

    def classification(self, sku: str = None) -> str:
        """ Classification state.

        Args:
            sku (str):   SKU unique identification.

        Returns:
            str:        New state.

        """
        inventory_class = ('AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ')
        classification_revenue = {}

        for i in inventory_class:
            for classifications in self.summarised_inventory.abc_xyz_summary(classification=(i,),
                                                                             category=('revenue',)):
                classification_revenue.update(deepcopy({i: classifications.get(i)['revenue']}))

        # response = 'The revenue by inventory classification can be broken down as: {breakdown}'.format(
        # **{'breakdown': ', '.join(['{}: {currency_symbol}{val:,.2f}'.format(key, **{'val':value},
        # **{'currency_symbol': self.currency}) for (key, value) in classification_revenue.items()])})

        response = 'The percentage contribution to revenue by classification of SKU, can be broken down as follows: ' \
                   '{breakdown} '.format(**{'breakdown': ', '.join(
            ['{}: {val:,.2f}%'.format(key, **{'val': (Decimal(value) / self.total_revenue) * 100}) for (key, value)
             in classification_revenue.items()])})
        self.append_response(response=response, sku=sku)
        top_revenue_classification = max(classification_revenue, key=lambda key: classification_revenue[key])

        if top_revenue_classification in ('AZ', 'BZ', 'CZ'):
            response = '{top} contributing the most to the inventory revenue may'.format(
                **{'top': top_revenue_classification})
            self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('EXCESS_STATE', self._END_STATE)
        return state

    def excess(self, sku: str = None) -> str:
        """ Excess state

        Args:
            sku (str):      SKU unique identification.

        Returns:
            str:            New state.

        """
        top_10_excess = [item for item in self.summarised_inventory.rank_summary(attribute='excess_stock',
                                                                                 count=10, reverse=True)]
        excess_skus = [i.get('sku') for i in top_10_excess]
        total_excess_cost = sum([Decimal(description.get('excess_cost')) for description in
                                 self.summarised_inventory.describe_sku(*excess_skus)])
        sku_inventory_turns = {excess_skus[index]: description.get('inventory_turns') for index, description in
                               enumerate(self.summarised_inventory.describe_sku(*excess_skus))}

        response = 'Focus on reducing the excess for the following {sku}. These SKU account for {cost} of excess cost. '.format(
            **{'sku': ", ".join(excess_skus)}, **{'cost': total_excess_cost})

        self.append_response(response=response, sku=sku)
        state = self._TRANSITION_STATES.get('SHORTAGE_STATE', self._END_STATE)
        return state

    def shortage(self, sku: str = None) -> str:

        top_10_shortage = [item for item in self.summarised_inventory.rank_summary(attribute='shortages',
                                                                                   count=10, reverse=True)]

        shortage_skus = [i.get('sku') for i in top_10_shortage]

        total_shortages = sum([Decimal(description.get('shortage_cost')) for description in
                               self.summarised_inventory.describe_sku(*shortage_skus)])

        top_10_revenue = self._rank_summary(attribute='revenue', count=10)
        top_10_revenue_skus = [summary.get('sku') for summary in top_10_revenue]

        shortage_skus_top_revenue = [i.get('sku') for i in top_10_shortage if i.get('sku') in top_10_revenue_skus]

        shortage_skus_top_revenue_total = sum([Decimal(description.get('revenue')) for description in
                                               self.summarised_inventory.describe_sku(*top_10_revenue_skus)])

        response = 'Consider increasing the stock holding of the following SKU: {sku}. ' \
                   'The total cost of covering the shortages is {cost}. ' \
                   'Give more consideration to SKUs {rev_sku} as they are particularly important, ' \
                   'they are in the top 10 contributors to yearly revenue, they contribute {contr_rev:.2f} which is ' \
                   '{perc: .2f}% of total revenue.'.format(
            **{'sku': ', '.join(shortage_skus)}, **{'cost': total_shortages},
            **{'rev_sku': ', '.join(shortage_skus_top_revenue)},
            **{'contr_rev': shortage_skus_top_revenue_total},
            **{'perc': (shortage_skus_top_revenue_total / self.total_revenue) * 100})

        self.append_response(response=response, sku=sku)

        state = self._TRANSITION_STATES.get('INVENTORY_STATE', self._END_STATE)
        return state

    def inventory_turns(self, sku: str = None) -> str:
        """ Inventory turns state.

        Args:
            sku (str):   SKU unique identification.

        Returns:
            str:         New state
        """
        skus = [i.sku_id for i in self.analysed_orders]

        sku_inventory_turns = {skus[index]: description.get('inventory_turns') for index, description in
                               enumerate(self.summarised_inventory.describe_sku(*skus))}

        sku_unit_cost = {skus[index]: description.get('unit_cost') for index, description in
                         enumerate(self.summarised_inventory.describe_sku(*skus))}

        slow_turners = heapq.nsmallest(5, sku_inventory_turns, key=lambda s: sku_inventory_turns[s])
        expensive_stock = heapq.nlargest(5, sku_unit_cost, key=lambda s: sku_inventory_turns[s])

        slow_turning_expensive_stock = [sku for sku in slow_turners if sku in expensive_stock]

        if len(slow_turning_expensive_stock) > 0:
            response = '{sku} experience the slowest inventory turns in the inventory profile, while simultaneously ' \
                       'being the most costly items.'
            self.append_response(response=response, sku=sku)

        serialise_config(configuration=self._compiled_response.shared_response,
                         file_path=ABS_FILE_PATH['PROFILE_PICKLE'])
        state = self._TRANSITION_STATES.get('RECOMMENDATION_STATE', self._END_STATE)
        return state
