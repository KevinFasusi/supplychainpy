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

import os
import uuid
from datetime import datetime

from sqlalchemy import (MetaData, create_engine, Table, Column, Integer, String, DateTime, ForeignKey)
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_ARCHIVE, ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG
from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy._helpers._pickle_config import serialise_config

TRANSACTION_TYPES = ['archive', 'compress']

metadata = MetaData()

transaction_type = Table('transaction_type', metadata,
                         Column('type_id', Integer(), primary_key=True),
                         Column('type', String(255)),
                         Column('create_date', DateTime(), default=datetime.now)
                         )

logged_transaction = Table('logged_transaction', metadata,
                           Column('log_id', Integer(), primary_key=True),
                           Column('type_id', ForeignKey('transaction_type.type_id')),
                           Column('create_date', DateTime(), default=datetime.now)

                           )

compressed_files = Table('compressed_files', metadata,
                         Column('compressed_id', Integer(), primary_key=True),
                         Column('compressed_file_path', String(255), nullable=False),
                         Column('compressed_file_name', String(255), nullable=False),
                         Column('create_date', DateTime(), default=datetime.now)
                         )

csv_files = Table('csv_files', metadata,
                  Column('file_id', Integer(), primary_key=True),
                  Column('file_path', String(255), nullable=False),
                  Column('analysis_id', Integer(), nullable=False),
                  Column('file_name', String(255), nullable=False),
                  Column('transaction_id', ForeignKey('logged_transaction.log_id')),
                  Column('compressed_file_id', ForeignKey('compressed_files.compressed_id')),
                  Column('create_date', DateTime(), default=datetime.now),
                  Column('update_date', DateTime(), default=datetime.now, onupdate=datetime.now)
                  )


# print(ABS_FILE_PATH, uuid.uuid1())

def create_management_db():
    connection = create_engine(database_connection_uri(db='management', create=True))
    metadata.create_all(connection)
    for i in TRANSACTION_TYPES:
        ins = transaction_type.insert().values(
            type=i
        )

        connection.execute(ins)
