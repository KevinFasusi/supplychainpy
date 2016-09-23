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
from sqlalchemy import select
from supplychainpy._helpers._db_connection import engine


def master_sku_list(uri: str):
    """Uses connection and reflects database object from table to execute query for all skus in master_sku table"""
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
