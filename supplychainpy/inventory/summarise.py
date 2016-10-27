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
from operator import attrgetter
from supplychainpy.inventory.abc_xyz import AbcXyz

from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand


class Inventory:
    def __init__(self, processed_orders):
        self.__analysed_orders = processed_orders
        self.__abc_xyz = self._abc_xyz_summary_raw()

    @property
    def abc_xyz_raw(self):
        return self.__abc_xyz

    def rank_summary(self, attribute: str, count: int = 0, reverse: bool = True) -> dict:
        """ Ranks any SKU in the profile by an attribute from the UncertainDemand objects orders_summary method.

        Args:
            attribute (str):    SKU attribute from analysed orders in UncertainDemand object
            count (int):        The running count required e.g. 10 for top 10.
            reverse (bool):     Reverse the rank order e.g. top 10 or bottom 10

        Returns:
            dict:               Ranked summary for attribute specified.

        """
        if count == 0:
            count = len(self.__analysed_orders)

        try:
            for index, sku in enumerate(sorted(self.__analysed_orders, key=attrgetter(attribute), reverse=reverse)):
                if index > count:
                    break
                yield sku.orders_summary()
        except AttributeError as e:
            possible_attributes = "Incorrect attribute provided as key. Please use one of the following:\n" \
                                  "demand_variability\neconomic_order_quantity\naverage_order\nsafety_stock" \
                                  "\nstandard_deviation\nreorder_level\nreorder_quantity\nrevenue\n" \
                                  "economic_order_quantity\neconomic_order_variable_cost\n" \
                                  "ABC_XYZ_Classification\nexcess_stock\nshortages\nquantity_on_hand"
            raise AttributeError(possible_attributes)

        except TypeError as e:
            print("Failed {}".format(e))

    def _abc_xyz_summary_raw(self):
        abc = AbcXyz(self.__analysed_orders)
        abc.classification_summary()
        # return total excess, shortages,
        return abc

    def abc_xyz_summary(self, classification: tuple = ('AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ'),
                        category: tuple = ('excess_stock', 'shortages', 'revenue'), value: str = 'currency') -> dict:
        """Retrieve currency value or units for key metrics by classification. Defaults to currency unless units stated.

        Args:
            classification (tuple):     ABCXYZ inventory classification of sku.
            category (tuple):           Category with which to aggregate the SKU classification.
            value (str):                Defaults to aggregating classification on currency unless units are specified.

        Returns:
            dict:                       Aggregated summary for classification based on category in
            currency value or units.

        """

        # Retrieves a subset of the orders analysis based on the classification (AX, AY, AZ...) held in dict

        style = {'AX': [analysis if self.__abc_xyz.ax is not None else 0 for analysis in self.__abc_xyz.ax],
                 'AY': [analysis if self.__abc_xyz.ay is not None else 0 for analysis in self.__abc_xyz.ay],
                 'AZ': [analysis if self.__abc_xyz.az is not None else 0 for analysis in self.__abc_xyz.az],
                 'BX': [analysis if self.__abc_xyz.bx is not None else 0 for analysis in self.__abc_xyz.bx],
                 'BY': [analysis if self.__abc_xyz.by is not None else 0 for analysis in self.__abc_xyz.by],
                 'BZ': [analysis if self.__abc_xyz.bz is not None else 0 for analysis in self.__abc_xyz.bz],
                 'CX': [analysis if self.__abc_xyz.cx is not None else 0 for analysis in self.__abc_xyz.cx],
                 'CY': [analysis if self.__abc_xyz.cy is not None else 0 for analysis in self.__abc_xyz.cy],
                 'CZ': [analysis if self.__abc_xyz.cz is not None else 0 for analysis in self.__abc_xyz.cz]}
        try:
            # filters the subset based on classification and category requested and return the currency vale of the

            temp_sum = Decimal(0)
            unit_cost = Decimal(0)

            temp_currency_summary = {}

            for id in classification:
                for label in category:
                    if label in ('excess_stock', 'shortages', 'revenue'):
                        summary = style.get(id)
                        for sku in summary:
                            unit_cost = Decimal(sku.get("unit_cost"))
                            t = {**sku}
                            temp_sum += Decimal(t.get(label))
                            t.clear()

                        if label == 'revenue':
                            temp_currency_summary.update({label: float(temp_sum)})

                        elif label != 'revenue' and value == 'currency':
                            temp_currency_summary.update({'{}_cost'.format(label): float(temp_sum * unit_cost)})

                        else:
                            temp_currency_summary.update({'{}_units'.format(label): float(temp_sum)})

                        temp_sum = 0
                    else:
                        raise TypeError

                yield {id: temp_currency_summary}
                #temp_currency_summary.clear()

        except TypeError as e:
            raise TypeError("abc_xyz_summary terminated {}".format(e))

        except AttributeError as e:
            print("Incorrect Category or Attribute empty. {}".format(e))

    def describe_sku(self, *args: str)->dict:
        """ Summarise SKU using descriptive statistics, key performance indicators, financial fundamentals and rankings

        Args:
            *args (str): SKU unique identification

        Returns:
            dict:   Summary of SKU.

        """
        try:
            for arg in args:
                yield self._summarise_sku(arg)

        except TypeError as e:
            raise TypeError(
                "SKU id {} is not valid, please make sure you supply the correct sku id. {}".format(args, e))

    def _summarise_sku(self, sku_id: str) -> dict:
        """Summarise SKU using descriptive statistics, key performance indicators and rankings.

        Args:
            sku_id (str):   SKU unique identification.

        Returns:
            dict:           Summary of SKU.

        """
        selection = UncertainDemand

        for sku in self.__analysed_orders:
            if sku.sku_id == sku_id:
                selection = sku
                break

        # If summary is updated also update possible attributes error in rank summary
        summary = {'sku_id': '{}'.format(selection.sku_id),
                   'revenue_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='revenue')),
                   'revenue': '{}'.format(selection.revenue),
                   'retail_price': '{}'.format(selection.retail_price),
                   'gross_profit_margin': '{}'.format(Decimal(selection.retail_price) - Decimal(selection.unit_cost)),
                   'markup_percentage': '{}'.format(
                       (Decimal(selection.retail_price) - selection.unit_cost) / selection.unit_cost),
                   'unit_cost': '{}'.format(selection.unit_cost),
                   'excess_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='excess_stock_cost')),
                   'excess_units': '{}'.format(selection.excess_stock),
                   'excess_cost': '{}'.format(Decimal(selection.excess_stock_cost)),
                   'shortage_rank': self._rank(sku_id=sku_id, attribute='shortage_cost'),
                   'shortage_units': '{}'.format(round(selection.shortages)),
                   'shortage_cost': '{}'.format(selection.shortage_cost),
                   'safety_stock_units': '{}'.format(round(selection.safety_stock)),
                   'safety_stock_cost': '{}'.format(selection.safety_stock_cost),
                   'safety_stock_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='safety_stock_cost')),
                   'classification': '{}'.format(selection.abcxyz_classification),
                   'average_orders': '{}'.format(round(selection.average_orders)),
                   'min_order': '{}'.format(min(map(int, selection.orders))),
                   'max_order': '{}'.format(max(map(int, selection.orders))),
                   'percentage_contribution_revenue': '{}'.format(selection.percentage_revenue),
                   'quantity_on_hand': '{}'.format(selection.quantity_on_hand),
                   'inventory_turns': '{}'.format((Decimal(selection.total_orders) * Decimal(selection.unit_cost)) / (
                       Decimal(selection.quantity_on_hand) * Decimal(selection.unit_cost))),
                   'inventory_traffic_light': '{}'.format(self._quantity_on_hand_alert(selection)),
                   'unit_cost_rank': self._rank(sku_id=sku_id, attribute='unit_cost'),
                   }
        # print(self._rank(sku_id=sku_id, attribute='shortage_cost'))
        return summary

    def _rank(self, sku_id: str, attribute: str) -> int:
        """ Rank SKU attributes against whole inventory profile.

        Args:
            sku_id (str):       SKU unique identification number.
            attribute (str):    Attribute keyword.

        Returns:
            int:    Attribute rank.

        """
        for index, t in enumerate(sorted(self.__analysed_orders, key=attrgetter(attribute), reverse=True)):
            if t.sku_id == sku_id:
                return index + 1

    def _quantity_on_hand_alert(self, selection: UncertainDemand) -> str:
        """ Indicates whether the quantity of units to hand is (quantity_on_hand < reorder_level(Amber)),
        (quantity_on_hand <50% safety_stock(Red)) and (quantity_on_hand < 75% safety stock(white)

        Args:
            selection (UncertainDemand): Analysed sku object.

        Returns:
            str:    Traffic light indicator summarising final inventory position for inventory quantity on hand.

        """

        half_safety_stock = float(selection.safety_stock) * 0.5
        two_thirds_safety_stock = float(selection.safety_stock) * 0.75
        if selection.reorder_level > selection.quantity_on_hand > selection.safety_stock:
            traffic_light = 'amber'
        elif half_safety_stock > selection.quantity_on_hand > two_thirds_safety_stock:
            traffic_light = 'red'
        elif selection.quantity_on_hand < two_thirds_safety_stock:
            traffic_light = 'white'
        else:
            traffic_light = 'green'

        return traffic_light

    def _currency_codes(self, code: str=None):
        codes = {"AED": u"\u062f"+ u"\u002e" + u"\u0625", "AFN": u"\u060B", "ALL": u"\u004C" + u"\u0065" + u"\u006B",
                 "AMD": "Armenia Dram", "ANG": "Netherlands Antilles Guilder", "AOA": "Angola Kwanza",
                 "ARS": "Argentina Peso", "AUD": "Australia Dollar", "AWG": "Aruba Guilder",
                 "AZN": "Azerbaijan New Manat", "BAM": "Bosnia and Herzegovina Convertible Marka",
                 "BBD": "Barbados Dollar", "BDT": "Bangladesh Taka", "BGN": "Bulgaria Lev", "BHD": "Bahrain Dinar",
                 "BIF": "Burundi Franc", "BMD": "Bermuda Dollar", "BND": "Brunei Darussalam Dollar",
                 "BOB": "Bolivia Bolíviano", "BRL": "Brazil Real", "BSD": "Bahamas Dollar",
                 "BTN": "Bhutan Ngultrum", "BWP": "Botswana Pula", "BYR": "Belarus Ruble", "BZD": "Belize Dollar",
                 "CAD": "Canada Dollar", "CDF": "Congo/Kinshasa Franc", "CHF": "Switzerland Franc",
                 "CLP": "Chile Peso", "CNY": "China Yuan Renminbi", "COP": "Colombia Peso",
                 "CRC": "Costa Rica Colon", "CUC": "Cuba Convertible Peso", "CUP": "Cuba Peso",
                 "CVE": "Cape Verde Escudo", "CZK": "Czech Republic Koruna", "DJF": "Djibouti Franc",
                 "DKK": "Denmark Krone", "DOP": "Dominican Republic Peso", "DZD": "Algeria Dinar",
                 "EGP": "Egypt Pound", "ERN": "Eritrea Nakfa", "ETB": "Ethiopia Birr",
                 "EUR": u"\u20ac", "FJD": "Fiji Dollar", "FKP": "Falkland Islands (Malvinas) Pound",
                 "GBP": u"\u00A3", "GEL": "Georgia Lari", "GGP": "Guernsey Pound",
                 "GHS": "Ghana Cedi", "GIP": "Gibraltar Pound", "GMD": "Gambia Dalasi", "GNF": "Guinea Franc",
                 "GTQ": "Guatemala Quetzal", "GYD": "Guyana Dollar", "HKD": "Hong Kong Dollar",
                 "HNL": "Honduras Lempira", "HRK": "Croatia Kuna", "HTG": "Haiti Gourde", "HUF": "Hungary Forint",
                 "IDR": "Indonesia Rupiah", "ILS": "Israel Shekel", "IMP": "Isle of Man Pound",
                 "INR": "India Rupee", "IQD": "Iraq Dinar", "IRR": "Iran Rial", "ISK": "Iceland Krona",
                 "JEP": "Jersey Pound", "JMD": "Jamaica Dollar", "JOD": "Jordan Dinar", "JPY": "Japan Yen",
                 "KES": "Kenya Shilling", "KGS": "Kyrgyzstan Som", "KHR": "Cambodia Riel", "KMF": "Comoros Franc",
                 "KPW": "Korea (North) Won", "KRW": "Korea (South) Won", "KWD": "Kuwait Dinar",
                 "KYD": "Cayman Islands Dollar", "KZT": "Kazakhstan Tenge", "LAK:": "Laos Kip",
                 "LBP": "Lebanon Pound", "LKR": "Sri Lanka Rupee", "LRD": "Liberia Dollar", "LSL": "Lesotho Loti",
                 "LYD": "Libya Dinar", "MAD": "Morocco Dirham", "MDL": "Moldova Leu", "MGA": "Madagascar Ariary",
                 "MKD": "Macedonia Denar", "MMK": "Myanmar (Burma) Kyat", "MNT": "Mongolia Tughrik",
                 "MOP": "Macau Pataca", "MRO": "Mauritania Ouguiya", "MUR": "Mauritius Rupee",
                 "MVR": "Maldives (Maldive Islands) Rufiyaa", "MWK": "Malawi Kwacha", "MXN": "Mexico Peso",
                 "MYR": "Malaysia Ringgit", "MZN": "Mozambique Metical", "NAD": "Namibia Dollar",
                 "NGN": "Nigeria Naira", "NIO": "Nicaragua Cordoba", "NOK:": "Norway Krone", "NPR": "Nepal Rupee",
                 "NZD": "New Zealand Dollar", "OMR": "Oman Rial", "PAB": "Panama Balboa", "PEN": "Peru Sol",
                 "PGK": "Papua New Guinea Kina", "PHP": "Philippines Peso", "PKR": "Pakistan Rupee",
                 "PLN": "Poland Zloty", "PYG": "Paraguay Guarani", "QAR": "Qatar Riyal", "RON": "Romania New Leu",
                 "RSD": "Serbia Dinar", "RUB": "Russia Ruble", "RWF": "Rwanda Franc", "SAR": "Saudi Arabia Riyal",
                 "SBD": "Solomon Islands Dollar", "SCR": "Seychelles Rupee", "SDG": "Sudan Pound",
                 "SEK": "Sweden Krona", "SGD": "Singapore Dollar", "SHP": "Saint Helena Pound",
                 "SLL": "Sierra Leone Leone", "SOS": "Somalia Shilling", "SPL:": "Seborga Luigino",
                 "SR:D": "Suriname Dollar", "STD": "São Tomé and Príncipe Dobra", "SVC": "El Salvador Colon",
                 "SYP": "Syria Pound", "SZL": "Swaziland Lilangeni", "THB": "Thailand Baht",
                 "TJS": "Tajikistan Somoni", "TMT": "Turkmenistan Manat", "TND": "Tunisia Dinar",
                 "TOP": "Tonga Pa'anga", "TRY": "Turkey Lira", "TTD": "Trinidad and Tobago Dollar",
                 "TVD": "Tuvalu Dollar", "TWD": "Taiwan New Dollar", "TZS": "Tanzania Shilling",
                 "UAH": "Ukraine Hryvnia", "UGX": "Uganda Shilling", "USD": u"\u0024",
                 "UYU": "Uruguay Peso", "UZS": "Uzbekistan Som", "VEF": "Venezuela Bolivar",
                 "VND": "Viet Nam Dong", "VUV": "Vanuatu Vatu", "WST": "Samoa Tala",
                 "XAF": "Communauté Financière Africaine (BEAC) CFA Franc BEAC", "XCD": "East Caribbean Dollar",
                 "XDR": "International Monetary Fund (IMF) Special Drawing Rights",
                 "XOF": "Communauté Financière Africaine (BCEAO) Franc",
                 "XPF": "Comptoirs Français du Pacifique (CFP) Franc", "YER": "Yemen Rial",
                 "ZAR": "South Africa Rand", "ZMW": "Zambia Kwacha", "ZWD": "Zimbabwe Dollar"}

        currency = codes.get('AED')

        return codes

if __name__ == '__main__':
    print('{}'.format(u"\u20ac"))