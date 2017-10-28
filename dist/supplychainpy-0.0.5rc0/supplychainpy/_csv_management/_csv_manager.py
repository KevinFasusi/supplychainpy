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
import sqlite3
import uuid
from shutil import copyfile

from sqlalchemy import create_engine
from supplychainpy._csv_management._controller._update_db import post_transaction
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG, ABS_FILE_PATH_ARCHIVE, \
    ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG
from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy._helpers._pickle_config import deserialise_config, serialise_config


class _Orchestrate:
    """Orchestrates the management of csv files used to generate the analysis uploaded to the database."""

    __file_path = ''

    def __init__(self):
        pass

    # Check config file for presence of existing management db if not create new one
    @staticmethod
    def check_for_db():
        """ Checks _archive directory for the presence of a csv_management database. If an csv_management database
            does not exist, then a new instance is created.

        Returns:
            bool:   Returns False indicating a database does exist and there is not a need to create one, or True
                    indicating a database does not exist and so one should be created.

        """
        config = deserialise_config(ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG)
        f = list([i.name for i in os.scandir(ABS_FILE_PATH_ARCHIVE)])
        #print(f,'\n', config.get('database_name', 'UNKNOWN'))
        if config.get('database_name', 'UNKNOWN') in f:
            return False
        else:
            return True

    @staticmethod
    def copy_file():
        """Copies file used to load analysis and stores in archive folder for posterity.

        Returns:

        """
        # Retrieve file_name and path to the source data csv
        config_file = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        file_name = config_file.get('file', 'UNKNOWN')
        file_path = config_file.get('database_path', 'UNKNOWN')
        print(file_path, file_name)
        if 'UNKNOWN' not in (file_path, file_name):
            try:
                # Copy data source file to archive
                copyfile('{}{}'.format(file_path, file_name),
                         '{}/{}-{}.csv'.format(ABS_FILE_PATH_ARCHIVE, 'data_file', uuid.uuid1()))
                config_file['file_path'] = '{}/{}-{}.csv'.format(ABS_FILE_PATH_ARCHIVE, 'data_file', uuid.uuid1())
                serialise_config(config_file, ABS_FILE_PATH_APPLICATION_CONFIG)

            except FileExistsError as e:
                print('The source file is not in the same location as the analysis database. Please place the file in '
                      'the same location and restart the process.')

    @staticmethod
    def update_database(analysis_id) -> bool:
        """Updates csv management database with

        Args:
            analysis_id (int):  The id for the analysis the data file corresponds to as given by the transaction table,
                                when running an analysis

        Returns:
            bool:  Success or failure for the updating of the csv_management database.

        """
        connection = create_engine(database_connection_uri(db='management', retrieve=True))
        return post_transaction(analysis_id=analysis_id, connection=connection)

    def archive_file(self):
        """ Compresses the files in the archive once the _archive directory reaches a specified size.

        Returns:
            bool:   Success or failure of archiving process

        """
        f = [i for i in os.scandir(ABS_FILE_PATH_ARCHIVE)]
        print(f[0])


if __name__ == '__main__':
    d = _Orchestrate()
    d.copy_file()
    d.update_database(analysis_id=1)
