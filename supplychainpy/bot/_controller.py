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

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
from supplychainpy._helpers._db_connection import engine


def master_sku_list(uri: str) -> list:
    """ Connects to database to retrieve master sku list.

    Args:
        uri (str): Database connection string.

    Returns:
        list:   All unique SKU identification.

    """
    meta = MetaData()
    connection = engine(uri)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id])
    rp = connection.execute(skus)
    result = []
    for i in rp:
        result.append((i['id'], i['sku_id']))
    rp.close()

    return result


def excess_controller(uri: str, direction: str = None, sku_id: str = None) -> tuple:
    """ Retrieves the excess SKUs in the inventory analysis table.

    Args:
        uri (str):          Database connection string.
        direction (str):    Indication of sort direction.
        sku_id (str):       SKU unique id.

    Returns:
        tuple:              Result.

    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    if direction == 'biggest':
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.excess_cost,
                       func.min(inventory_analysis.columns.excess_rank)])
    else:
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.excess_cost,
                       func.max(inventory_analysis.columns.excess_rank)])

    # for i in inventory_analysis.columns:
    #    print(i)
    rp = connection.execute(skus)
    result = []
    sku_id = ""
    for i in rp:
        sku_id = str(i['sku_id'])
        result.append((i['sku_id'], i['excess_cost']))
    rp.close()
    # print(sku_id)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id]).where(msk_table.columns.id == sku_id)
    rp = connection.execute(skus)
    for i in rp:
        result.append(i['sku_id'])
    rp.close()

    return tuple(result)


def shortage_controller(uri: str, direction: str = None, sku_id: str = None) -> tuple:
    """ Retrieves SKUs with shortages.

    Args:
        uri (str):          Database connection string.
        direction (str):    Indication of sort direction.
        sku_id (str):       SKU unique id.

    Returns:
        tuple:              Result.


    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)

    if direction == 'biggest':
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.shortage_cost,
                       func.min(inventory_analysis.columns.shortage_rank)])
    else:
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.shortage_cost,
                       func.max(inventory_analysis.columns.shortage_rank)])

    rp = connection.execute(skus)
    result = []
    sku_id = ""
    for i in rp:
        sku_id = str(i['sku_id'])
        result.append((i['sku_id'], i['shortage_cost']))
    rp.close()
    # print(sku_id)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id]).where(msk_table.columns.id == sku_id)
    rp = connection.execute(skus)
    for i in rp:
        result.append(i['sku_id'])
    rp.close()
    return tuple(result)


def revenue_controller(uri: str, direction: str = None, sku_id: str = None) -> tuple:
    """ Retrieves SKUs which generate revenue.

    Args:
        uri (str):          Database connection string.
        direction (str):    Indication of sort direction.
        sku_id (str):       SKU unique id.

    Returns:
        tuple:              Result.


    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)

    if direction == 'smallest':
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.revenue,
                       func.min(inventory_analysis.columns.revenue)])
    else:
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.revenue,
                       func.max(inventory_analysis.columns.revenue)])

    rp = connection.execute(skus)
    result = []
    sku_id = ""
    for i in rp:
        sku_id = str(i['sku_id'])
        result.append((i['sku_id'], i['revenue']))
    rp.close()
    # print(sku_id)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id]).where(msk_table.columns.id == sku_id)
    rp = connection.execute(skus)
    for i in rp:
        result.append(i['sku_id'])
    rp.close()
    return tuple(result)


def inventory_turns_controller(uri: str, direction: str = None, sku_id: str = None) -> tuple:
    """ Retrieves SKU's Inventory Turns.

    Args:
        uri (str):          Database connection string.
        direction (str):    Indication of sort direction.
        sku_id (str):       SKU unique id.

    Returns:
        tuple:              Result.

    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    if direction == 'smallest':
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.inventory_turns,
                       func.min(inventory_analysis.columns.inventory_turns)])
    else:
        skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.inventory_turns,
                       func.max(inventory_analysis.columns.inventory_turns)])

    rp = connection.execute(skus)
    result = []
    sku_id = ""
    for i in rp:
        sku_id = str(i['sku_id'])
        result.append((i['sku_id'], i['inventory_turns']))
    rp.close()
    # print(sku_id)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id]).where(msk_table.columns.id == sku_id)
    rp = connection.execute(skus)
    for i in rp:
        result.append(i['sku_id'])
    rp.close()
    return tuple(result)


def average_orders_controller(uri: str, direction: str = None, sku_id: str = None) -> tuple:
    """ Retrieves SKU's average orders.

    Args:
        uri (str):          Database connection string.
        direction (str):    Indication of sort direction.
        sku_id (str):       SKU unique id.

    Returns:
        tuple:              Result.

    """
    rp = None
    try:
        meta = MetaData()
        connection = engine(uri)
        inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
        if direction == 'smallest':
            skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.average_orders,
                           func.min(inventory_analysis.columns.average_orders)])
        else:
            skus = select([inventory_analysis.columns.sku_id, inventory_analysis.columns.average_orders,
                           func.max(inventory_analysis.columns.average_orders)])

        rp = connection.execute(skus)
        result = []
        sku_id = ""
        for i in rp:
            sku_id = str(i['sku_id'])
            result.append((i['sku_id'], i['average_orders']))
        rp.close()
        # print(sku_id)
        msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
        skus = select([msk_table.columns.id, msk_table.columns.sku_id]).where(msk_table.columns.id == sku_id)
        rp = connection.execute(skus)
        for i in rp:
            result.append(i['sku_id'])

        return tuple(result)
    finally:
        rp.close()


def currency_symbol_controller(uri: str) -> str:
    """ Retrieves currency code from analysis database.

    Args:
        uri (str):          Database connection string.

    Returns:
        tuple:              Result.

    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    transaction_log = Table('transaction_log', meta, autoload=True, autoload_with=connection)
    most_recent_transaction = select([transaction_log.columns.id, func.max(transaction_log.columns.date)]).limit(1)
    rp = connection.execute(most_recent_transaction)
    transaction_id = 0
    for i in rp:
        transaction_id = i['id']
    symbol_id = select([inventory_analysis.columns.currency_id]).where(
        inventory_analysis.columns.transaction_log_id == transaction_id).limit(1)
    rp.close()
    rp = connection.execute(symbol_id)
    currency_symbol_id = 0
    for i in rp:
        currency_symbol_id = i['currency_id']
    rp.close()
    currency = Table('currency', meta, autoload=True, autoload_with=connection)
    currency_symbol = select([currency.columns.currency_code]).where(currency.columns.id == currency_symbol_id)
    rp = connection.execute(currency_symbol)
    currency_code = 0
    for i in rp:
        currency_code = i['currency_code']
    rp.close()
    return currency_code


def classification_controller(uri: str, sku_id: str = None) -> tuple:
    """ Retrieves inventory classification for SKU.

    Args:
        uri (str):      Database connection string.
        sku_id (str):   SKU unique identification.

    Returns:
        tuple:  Result.

    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    msk = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    j = join(inventory_analysis, msk, msk.columns.id == inventory_analysis.columns.sku_id)
    sku_classification = select([inventory_analysis.columns.abc_xyz_classification]).select_from(j).where(
        msk.columns.sku_id == sku_id)
    rp = connection.execute(sku_classification)
    classification = ''
    for i in rp:
        classification = i['abc_xyz_classification']

    return classification

    # if using html currency symbols think about how to deal with ascii when iteracting with dash on the command line etc


def safety_stock_controller(uri: str, sku_id: str = None, direction: str = None):
    """ Retrieves safety stock.

    Args:
        uri (str):          Database connection string.
        sku_id (str):       SKU unique identification.
        direction (str):    Indication of sort direction.

    Returns:

    """

    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    msk = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    j = join(inventory_analysis, msk, msk.columns.id == inventory_analysis.columns.sku_id)

    if direction == 'smallest':
        sku_classification = select([func.min(inventory_analysis.columns.safety_stock),
                                     msk.columns.sku_id]).select_from(j)
        rp = connection.execute(sku_classification)
    else:
        sku_classification = select([func.max(inventory_analysis.columns.safety_stock),
                                     msk.columns.sku_id]).select_from(j)

        rp = connection.execute(sku_classification)

    safety_stock = ''
    for i in rp:
        safety_stock = i[0]
        sku_identification = i[1]

    return safety_stock, sku_identification


def reorder_level_controller(uri: str, sku_id: str = None, direction: str = None):
    """ Retrieves reorder level.

    Args:
        uri:
        sku_id:
        direction:

    Returns:

    """
    meta = MetaData()
    connection = engine(uri)
    inventory_analysis = Table('inventory_analysis', meta, autoload=True, autoload_with=connection)
    msk = Table('master_sku_list', meta, autoload=True, autoload_with=connection)
    j = join(inventory_analysis, msk, msk.columns.id == inventory_analysis.columns.sku_id)

    if direction == 'smallest':
        sku_classification = select([func.min(inventory_analysis.columns.reorder_level),
                                     msk.columns.sku_id]).select_from(j)
        rp = connection.execute(sku_classification)
    else:
        sku_classification = select([func.max(inventory_analysis.columns.reorder_level),
                                     msk.columns.sku_id]).select_from(j)
        rp = connection.execute(sku_classification)

    reorder_level = ''
    sku_identification = ''
    for i in rp:
        reorder_level = i[0]
        sku_identification = i[1]

    return reorder_level, sku_identification
