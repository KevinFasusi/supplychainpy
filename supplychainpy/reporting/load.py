import datetime
import os

from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.inventory.summarise import OrdersAnalysis
from supplychainpy.reporting.views import db
from supplychainpy.reporting.views import TransactionLog
from supplychainpy.reporting.views import InventoryAnalysis
from supplychainpy.reporting.views import MasterSkuList
from supplychainpy.reporting.views import Currency


def currency_codes():
    codes = {"AED": "United Arab Emirates Dirham", "AFN": "Afghanistan Afghani", "ALL": "Albania Lek",
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
             "EUR": "Euro Member Countries", "FJD": "Fiji Dollar", "FKP": "Falkland Islands (Malvinas) Pound",
             "GBP": "United Kingdom Pound", "GEL": "Georgia Lari", "GGP": "Guernsey Pound",
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
             "UAH": "Ukraine Hryvnia", "UGX": "Uganda Shilling", "USD": "United States Dollar",
             "UYU": "Uruguay Peso", "UZS": "Uzbekistan Som", "VEF": "Venezuela Bolivar",
             "VND": "Viet Nam Dong", "VUV": "Vanuatu Vatu", "WST": "Samoa Tala",
             "XAF": "Communauté Financière Africaine (BEAC) CFA Franc BEAC", "XCD": "East Caribbean Dollar",
             "XDR": "International Monetary Fund (IMF) Special Drawing Rights",
             "XOF": "Communauté Financière Africaine (BCEAO) Franc",
             "XPF": "Comptoirs Français du Pacifique (CFP) Franc", "YER": "Yemen Rial",
             "ZAR": "South Africa Rand", "ZMW": "Zambia Kwacha", "ZWD": "Zimbabwe Dollar"}
    return codes


def load(file_path: str):
    db.create_all()
    fx = currency_codes()
    for key, value in fx.items():
        codes = Currency()
        codes.country = value
        codes.currency_code = key
        db.session.add(codes)
    db.session.commit()
    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path,
                                                                      z_value=Decimal(1.28),
                                                                      reorder_cost=Decimal(5000),
                                                                      file_type="csv", length=12)

    ia = [analysis.orders_summary() for analysis in
          model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv", length=12)]
    date_now = datetime.datetime.now()
    analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)

    transact = TransactionLog()
    transact.date = date_now
    db.session.add(transact)
    db.session.commit()

    transaction_sub = db.session.query(db.func.max(TransactionLog.date))
    transaction_id = db.session.query(TransactionLog).filter(TransactionLog.date == transaction_sub).first()

    for item in ia:
        skus_description = [summarised for summarised in analysis_summary.describe_sku(item['sku'])]
        denom = db.session.query(Currency.id).filter(Currency.currency_code == item['currency']).first()
        master_sku = MasterSkuList()
        master_sku.sku_id = item['sku']
        db.session.add(master_sku)
        i_up = InventoryAnalysis()
        mk = db.session.query(MasterSkuList.id).filter(MasterSkuList.sku_id == item['sku']).first()
        i_up.sku_id = mk.id
        i_up.abc_xyz_classification = item['ABC_XYZ_Classification']
        i_up.standard_deviation = item['standard_deviation']
        i_up.safety_stock = item['safety_stock']
        i_up.reorder_level = item['reorder_level']
        i_up.economic_order_quantity = item['economic_order_quantity']
        i_up.demand_variability = item['demand_variability']
        i_up.average_orders = item['average_orders']
        i_up.shortages = item['shortages']
        i_up.excess_stock = item['excess_stock']
        i_up.reorder_quantity = item['reorder_quantity']
        i_up.economic_order_variable_cost = item['economic_order_variable_cost']
        i_up.unit_cost = item['unit_cost']
        i_up.revenue = item['revenue']
        i_up.date = date_now
        i_up.sa = skus_description[0]['safety_stock_rank']
        i_up.safety_stock_rank = skus_description[0]['shortage_rank']
        i_up.excess_cost = skus_description[0]['excess_cost']
        i_up.percentage_contribution_revenue = skus_description[0]['percentage_contribution_revenue']
        i_up.excess_rank = skus_description[0]['excess_rank']
        i_up.retail_price = skus_description[0]['retail_price']
        i_up.gross_profit_margin = skus_description[0]['gross_profit_margin']
        i_up.min_order = skus_description[0]['min_order']
        i_up.safety_stock_cost = skus_description[0]['safety_stock_cost']
        i_up.revenue_rank = skus_description[0]['revenue_rank']
        i_up.markup_percentage = skus_description[0]['markup_percentage']
        i_up.max_order = skus_description[0]['max_order']
        i_up.shortage_cost = skus_description[0]['shortage_cost']
        i_up.quantity_on_hand = item['quantity_on_hand']
        i_up.currency_id = denom.id
        i_up.transaction_log_id = transaction_id.id
        db.session.add(i_up)
    db.session.commit()


if __name__ == '__main__':
    rel_path = 'data2.csv'
    app_dir = os.path.dirname(__file__, )
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
    load(abs_file_path)
