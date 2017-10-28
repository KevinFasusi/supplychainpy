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

from sqlalchemy.engine import RowProxy
from sqlalchemy.sql import select

from supplychainpy._csv_management._model._db_setup import (csv_files, transaction_type, logged_transaction)
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config


def _retrieve_transaction_type(t_type: str, connection) -> RowProxy:
    """ Retrieves Transaction Type

    Args:
        ttype (str):     The transaction type that represents the trasaction being recorded 'archive' or 'compress'.

    Returns:
        RowProxy:    The transaction_type


    """
    transaction = select([transaction_type.c.type_id]).where(transaction_type.c.type == t_type)

    rp = connection.execute(transaction)
    record = rp.first()
    return record


def post_transaction(analysis_id, connection) -> bool:
    """ Inserts transaction record into csv_management database

    Args:
        analysis_id:    The id for the analysis the data file corresponds to as given by the transaction table,
                        when running an analysis
        connection:     Database connection for controller to use.

    Returns:
        bool:           True for completed transaction and False for failes transaction

    """
    try:
        # Inserts new transaction into transaction log
        transc_type = _retrieve_transaction_type(t_type='archive', connection=connection)
        tr = [i for i in transc_type]
        ins = logged_transaction.insert().values(
            type_id=tr[0]
        )

        result = connection.execute(ins)
        config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)

        # when file has been copied to archive location the file path should be updated.
        ins = csv_files.insert().values(
            file_path=config.get('file_path'),
            analysis_id=analysis_id,
            file_name='Inventory',
            transaction_id=result.inserted_primary_key[0]
        )

        connection.execute(ins)
        return True
    except OSError:
        return False


if __name__ == '__main__':
    # _retrieve_transaction_type('archive')
    post_transaction(1)
