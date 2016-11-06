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

from supplychainpy._helpers._pickle_config import deserialise_config, serialise_config
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG, ABS_FILE_PATH_ARCHIVE
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG
from sqlalchemy import create_engine

# Centralises all the construction of connections to the various database bases.

case = {

    'UNKNOWN': 'unknown',
    'REPORTING': 'reporting',
    'MANAGEMENT': 'management',
    'POSIX': 'posix',
    'MACINTOSH': 'mac',
    'NT': 'nt',
    'RETRIEVAL': 'retrieval',
    'CREATE': 'create'
}


def database_connection_uri(db: str = 'reporting', **kwargs) -> str:
    """ Manages the construction of a database uri for the purposes of connecting to a database.

    Args:
        db:     The string indicating 'reporting' or 'management' database uri.

    Returns:
        str:    database uri.

    """
    retrieve = kwargs.get('retrieve', False)
    create = kwargs.get('create', False)

    db_uri = ''

    unix, windows = [case['POSIX'], case['MACINTOSH']], [case['NT']]

    if retrieve:
        if db == case['REPORTING']:
            if os.name in unix:
                db_uri = _os_specific_uri(action_case=case['RETRIEVAL'], my_os=unix, type_case=case['REPORTING'])
            elif os.name in windows:
                db_uri = _os_specific_uri(action_case=case['RETRIEVAL'], my_os=windows, type_case=case['REPORTING'])
            return db_uri
        elif db == case['MANAGEMENT']:
            if os.name in unix:
                db_uri = _os_specific_uri(action_case=case['RETRIEVAL'], my_os=unix, type_case=case['MANAGEMENT'])
            elif os.name in windows:
                db_uri = _os_specific_uri(action_case=case['RETRIEVAL'], my_os=windows, type_case=case['MANAGEMENT'])
            return db_uri
        else:
            raise Exception("Incorrect database specified. Please select 'reporting' or 'management' ")
    elif create:
        if db == case['MANAGEMENT']:
            if os.name in unix:
                db_uri = _os_specific_uri(action_case=case['CREATE'], my_os=unix, type_case=case['MANAGEMENT'])
            elif os.name in windows:
                db_uri = _os_specific_uri(action_case=case['CREATE'], my_os=windows, type_case=case['MANAGEMENT'])
            return db_uri
    else:
        pass


# TODO-fix decide how the my_os variable should simplify this function, splitting the logic has increased lines of code.
def _os_specific_uri(action_case: str, my_os: list, type_case: str) -> str:
    """ Constructs os specific uri.
    Args:
        action_case:    The action base indicates wheter the connection is for retrieving from or creating a database
        my_os:          The os the user is running the library on.
        type_case:      Indicates wether the uri is for the csv management database or the reporting database

    Returns:

    """

    app_config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
    man_config = deserialise_config(ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG)
    db_uri = ''
    unix, windows = [case['POSIX'], case['MACINTOSH']], [case['NT']]

    if action_case == case['RETRIEVAL'] and type_case == case['REPORTING']:
        if os.name in unix:
            db_uri = 'sqlite:///{}/reporting.db'.format(app_config['database_path'])
        elif os.name in windows:
            db_uri = 'sqlite:///{}\\reporting.db'.format(app_config['database_path'])
        return db_uri
    elif action_case == case['RETRIEVAL'] and type_case == case['MANAGEMENT']:
        if os.name in unix:
            db_uri = 'sqlite:///{}/{}'.format(man_config['database_path'], man_config['database_name'])
        elif os.name in windows:
            db_uri = 'sqlite:///{}\\{}'.format(man_config['database_path'], man_config['database_name'])
        return db_uri
    elif action_case == case['CREATE'] and type_case == case['MANAGEMENT']:
        database_name = 'csv_management-{}.db'.format(uuid.uuid1())
        if os.name in unix:
            db_uri = 'sqlite:///{}/{}'.format(ABS_FILE_PATH_ARCHIVE, database_name)
        elif os.name in windows:
            db_uri = 'sqlite:///{}\\{}'.format(ABS_FILE_PATH_ARCHIVE, database_name)

        config = {
            'database_path': ABS_FILE_PATH_ARCHIVE,
            'database_name': database_name,
            'database_connection': db_uri
        }
        serialise_config(configuration=config, file_path=ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG)

        return db_uri


def engine(uri):
    cr_engine = create_engine(uri)
    return cr_engine


if __name__ == '__main__':
    print(database_connection_uri('management', retrieve='retrieve'))
