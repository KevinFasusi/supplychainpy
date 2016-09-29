from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.sample_data.config import ABS_FILE_PATH


class ResponseBorg:
    """ Borg class making  class attributes global """
    _shared_response = {}  # global attribute dictionary remember to use single under score not double

    def __init__(self):
        self.__dict__ = self._shared_response


class ResponseSingleton(ResponseBorg):
    def __init__(self, **kwargs):
        # borg class instantiated at same time as the singleton updates the
        # shared_state dictionary by adding a new key-value pair
        ResponseBorg.__init__(self)
        self._shared_response.update(kwargs)

    @property
    def shared_response(self) -> dict:
        return self._shared_response

    def __str__(self):
        # returns the attribute for printing
        return str(self._shared_response)


class SKUStates:
    def __init__(self, analysed_orders: UncertainDemand, forecast: dict = None):
        self.__analysed_orders = analysed_orders
        self.summarised_inventory = Inventory(analysed_orders)
        self._htces_forecast = forecast
        self._summary = {}
        self._compiled_response = ResponseSingleton()

    def initialise_machine(self, sku):
        self._summary = [description for description in
                         self.summarised_inventory.describe_sku(sku)][0]
        if int(self._summary.get('excess_units')) > 0:
            state = 'excess_rank'
        elif int(self._summary.get('shortage_units')) > 0:
            state = 'shortage_rank'
        else:
            state = 'inventory_turns'
        return state, sku

    def _append_response(self, response, sku):

        resp = self._compiled_response.shared_response.get(sku, 'EMPTY')
        if 'EMPTY' != resp:
            response = resp + response
            self._compiled_response.shared_response.update(**{'{}'.format(sku): response})
        else:
            self._compiled_response.shared_response.update(**{'{}'.format(sku): response})

    def excess_rank(self, sku):
        if int(self._summary.get('excess_rank', 11)) <= 10:
            response = '{} is one of the top 10 overstocked SKUs in your inventory profile, ranked {} of ' \
                       '10 overstocked SKUs. '.format(sku, sku, self._summary.get('excess_rank'))

            self._append_response(response=response, sku=sku)
            if self._summary.get('classification') == 'AX':
                response = 'The {} inventory classification indicates a stable demand profile. ' \
                           'SKU {} is in the 20% of SKU\'s that contribute 80% yearly revenue. ' \
                           'Unless {} product is approaching end of life (EOL)' \
                           ', there is likely little need to panic. ' \
                           'Holding purchase orders for this SKU will reduce ' \
                           'the excess. Review consumption of this SKU until the quantity on hand, ' \
                           'currently {}, is close to or below the reorder level of {}. '.format(
                            self._summary.get('classification'), sku, sku, self._summary.get('quantity_on_hand'),
                            self._summary.get('reorder_quantity'))

                self._append_response(response=response, sku=sku)

        state = 'inventory_turns'
        return state, sku

    def shortage_rank(self, sku):
        if int(self._summary.get('shortage_rank', 11)) <= 10:
            response = '{} is one of the top 10 understocked SKUs ' \
                       'in your inventory profile. {} is currently ranked {} of ' \
                       '10 understocked SKUs. '.format(sku, sku, self._summary.get('shortage_rank'))
            self._append_response(response=response, sku=sku)

        state = 'inventory_turns'
        return state, sku

    def inventory_turns(self, sku):
        if float(self._summary.get('inventory_turns')) <= 2.00 and int(self._summary.get('excess_rank', 11)) <= 10:
            response = '{} has a very low rolling inventory turn rate at {:.2f}. {} may be a greater cause for ' \
                       'concern considering it is also in the top 10 overstocked ' \
                       'SKUs in the inventory profile. '.format(sku, float(self._summary.get('inventory_turns')), sku)

            self._append_response(response=response, sku=sku)
        elif float(self._summary.get('inventory_turns')) <= 2.00:
            response = '{} has a very low rolling inventory turn rate at {:.2f}. '.format(
                sku, float(self._summary.get('inventory_turns')))
            self._append_response(response=response, sku=sku)
        state = 'classification'
        return state, sku

    def classification(self, sku):

        if self._summary.get('classification') in ('AZ', 'BZ', 'CZ'):
            response = 'The {} classification indicates that {} has volatile demand, ' \
                       'making it difficult to predict' \
                       ' the consumption of the excess. '.format(self._summary.get('classification'), sku)
            self._append_response(response=response, sku=sku)

        if self._summary.get('classification') == 'CZ' and self._summary.get('unit_cost_rank') < 10 \
                and int(self._summary.get('excess_rank', 11)) <= 10:
            response = '{} is a slow moving volatile SKU. A unit cost of {} makes it also one of the more costly' \
                       ' in the inventory profile.  ' \
                       'It may be prudent to make financial provisions for this product, ' \
                       'discount them or bundle them with a complimentary popular product ' \
                       'in a promotion. '.format(sku, self._summary.get('unit_cost'))
            self._append_response(response=response, sku=sku)
        if self._summary.get('classification') in ('AX', 'BX'):
            response = 'The {} classification, indicates that {} has a stable demand profile and ' \
                       'contributes significantly to revenue. ' \
                       'Corrective action should be taken to bring the quantity on hand (QOH) up from {} to {}. '
            self._append_response(response=response, sku=sku)

        state = 'traffic_light'

        return state, sku

    def traffic_light(self, sku):
        if self._summary.get('inventory_traffic_light') == 'white':
            response = 'The QOH is less than 75% of safety stock, implying a substantial quantity of buffer stock has '\
                       'been consumed. Take into consideration that it is acceptable ' \
                       'to dip into safety stock approximately 50% of the time. However, this situation ' \
                       'poses a threat for servicing future demand. This situation may be acceptable if this product ' \
                       'is \'end of life\' and the goal is to drive down stock. Corrective action is ' \
                       'required if it is not currently a policy to reduce the QOH for {}, and the ' \
                       'receipt of a purchase order is not imminent. '.format(sku)
            self._append_response(response=response, sku=sku)
        elif self._summary.get('inventory_traffic_light') == 'red':
            response = 'The QOH is is less 50% of the recommended safety stock. ' \
                       'Take into consideration that it is acceptable ' \
                       'to dip into safety stock approximately 50% of the time, consuming ' \
                       'approximately 50% of its value.' \
                       'Therefore, in this situation there may be little imminent threat to the service level. ' \
                       'Checking that a purchase order has been placed may be prudent. '.format(sku)
            self._append_response(response=response, sku=sku)
        elif self._summary.get('inventory_traffic_light') == 'amber':
            response = 'The QOH is is less than the reorder level but has yet to hit safety stock. ' \
                       'There is little to worry about at this point. The periodic review of stock ' \
                       'and communication of any upcoming deals or promotions ' \
                       'that may significantly impact the demand profile should be a focus.'
            self._append_response(response=response, sku=sku)
        elif self._summary.get('inventory_traffic_light') == 'green' and int(self._summary.get('excess_units', 11)) == 0\
                and self._summary.get('classification') not in ('CZ', 'CY', 'BZ', 'AZ') and\
                int(self._summary.get('shortage_units', 11)) == 0:

            response = 'Congratulations the QOH is within optimal boundaries.  ' \
                       'There is little to worry about at this point. The periodic review of stock ' \
                       'and communication of any upcoming deals or promotions that may significantly ' \
                       'impact the demand profile should be a focus. '
            self._append_response(response=response, sku=sku)
        state = 'forecast'
        return state, sku

    def forecast(self, sku):
        # if the demand shows a linear trend then check if the forecast is less than the excess units.
        if self._htces_forecast.get(sku)['statistics']['trend']:
            if self._htces_forecast.get(sku)['forecast'][0] < int(self._summary.get('excess_units')):
                response = 'It is unlikely {} will fair better next month as the most optimistic forecast is '
                self._append_response(response=response, sku=sku)
        if self._htces_forecast.get(sku)['statistics']['trend'] and int(self._summary.get('excess_units')) > 0 and \
                        self._summary.get('classification') in ('AX', 'AY', 'BX', 'BY', 'CX') and \
                        self._htces_forecast.get(sku)['forecast'][0] > int(self._summary.get('excess_units')):
            response = 'The current excess can be reduced by reducing purchase orders and allow the ' \
                       'forecasted demand to be catered for from stock. '
            self._append_response(response=response, sku=sku)
        state = 'recommendation'
        serialise_config(configuration=self._compiled_response.shared_response,
                         file_path=ABS_FILE_PATH['RECOMMENDATION_PICKLE'])
        return state, sku

class ProfileStates:
    def __init__(self, analysed_orders: UncertainDemand, forecast: dict = None):
        self.__analysed_orders = analysed_orders
        self.summarised_inventory = Inventory(analysed_orders)
        self._htces_forecast = forecast
        self._summary = {}
        self._compiled_response = ResponseSingleton()

