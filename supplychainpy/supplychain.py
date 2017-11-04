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

import argparse
import os
import pickle

import sys

import logging

from supplychainpy._csv_management._csv_manager import _Orchestrate
from supplychainpy._csv_management._model._db_setup import create_management_db
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._decorators import quiet_console
from supplychainpy._helpers._pickle_config import serialise_config, deserialise_config
from supplychainpy.bot.dash import ChatBot
from supplychainpy.launch_reports import launch_load_report, launch_report_server
from supplychainpy.launch_reports import launch_report
from supplychainpy.launch_reports import load_db

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def main():
    parser = argparse.ArgumentParser(description='Supplychainpy commandline interface a')

    parser.add_argument(dest='filenames', metavar='filename', nargs='?')

    parser.add_argument('-l', '--launch', dest='launch', action='store_true',
                        help='Launches supplychainpy reporting gui for setting \
                        port and launching the default browser.')

    parser.add_argument('-lx', '--launch-console', dest='launch_console', action='store_true',
                        help='Launches supplychainpy reporting in the default browser, \
                        without gui interface. Uses default port (5000) unless another port \
                        is specified. ')

    parser.add_argument('-a', '--analyse', dest='analyse_file', action='store_true',
                        help='Processes the file supplied as the first argument \
                        and performs analysis')

    parser.add_argument('-o', dest='outfile', action='store',
                        help='output file')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='verbose mode')

    parser.add_argument('-db', dest='database', action='store',
                        help='database engine uri e.g. ')

    parser.add_argument('-cur', dest='currency', action='store',
                        help='Sets the currency for the analysis. The currency should \
                        match the currency of the raw data. IMPORTANT: Currency \
                        conversion does not occur by setting this flag. The default \
                        currency is US Dollars (USD). ', default='USD')

    parser.add_argument('--host', dest='host', action='store',
                        help='Sets the host for the server \
                        (defaults 127.0.0.1) ', default='127.0.0.1')

    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Runs in debug mode (default : debug.INFO)')

    parser.add_argument('-loc', dest='location', action='store',
                        help='database path e.g. ')

    parser.add_argument('-u', dest='user', action='store',
                        help='user name ')

    parser.add_argument('-p', '--port', dest='port', action='store',
                        help='port to use for local server e.g. 8080 \
                        (default: 5000)', default='5000')

    parser.add_argument('-c', dest='chat', action='store_true',
                        help='chat to dash from the command line')

    args = parser.parse_args()

    if args.verbose:
        print('filenames = {}'.format(args.filenames))
        print('launch reports = {}'.format(args.launch))
        print('process file = {}'.format(args.analyse_file))
        print('database location = {}'.format(args.location))

    if args.debug:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    if args.launch and args.analyse_file is None and args.filenames is not None and args.location:
        # -l -loc
        print(1)

        if args.currency is not None:
            currency = args.currency
        else:
            currency = 'USD'
        app_settings = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        app_settings['database_path'] = args.location
        app_settings['file'] = args.filenames
        app_settings['currency'] = currency

        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
        #d = _Orchestrate()
        #d.copy_file()
        #db_present = d.check_for_db()
        #if db_present:
        #    create_management_db()
        launch_load_report(args.filenames, args.location)

    elif args.launch and args.analyse_file and args.filenames is not None and args.location is not None:
        # -a -loc -l
        print(2)

        if args.currency is not None:
            currency = args.currency
        else:
            currency = 'USD'
        app_settings = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        app_settings['database_path'] = args.location
        app_settings['file'] = args.filenames
        app_settings['currency'] = currency

        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
        #d = _Orchestrate()
        #d.copy_file()
        #db_present = d.check_for_db()
        #if db_present:
        #    create_management_db()
        launch_load_report(args.filenames, args.location)

    elif args.launch and args.location is not None and args.host:
        # -l -loc --host
        print(3)

        app_settings = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)

        app_settings['database_path'] = args.location
        app_settings['port'] = args.port
        app_settings['host'] = args.host,
        app_settings['currency'] = args.currency

        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)

        launch_report(location=args.location, host=args.host, port=args.port)

    elif args.launch and args.analyse_file and args.filenames and args.location:
        # -a -l -loc
        print(4)

        if args.currency is not None:
            currency = args.currency
        else:
            currency = 'USD'

        app_settings = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        app_settings['database_path'] = args.location
        app_settings['file'] = args.filenames
        app_settings['currency'] = currency

        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
        #d = _Orchestrate()
        #d.copy_file()
        #db_present = d.check_for_db()
        #if db_present:
        #    create_management_db()
        launch_load_report(args.filenames, args.location)
        launch_report(location=args.location, host=args.host, port=args.port)

    elif args.analyse_file and args.location is not None and args.filenames is not None and args.launch_console is None:
        print(8)
        # -a
        app_settings = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        app_settings['database_path'] = args.location
        app_settings['file'] = args.filenames
        load_db(file=args.filenames, location=args.location)

    elif args.analyse_file and args.location and args.filenames and args.launch_console and args.port:
        # -a -loc --lx -p
        try:
            print(5)
            app_settings = {
                'database_path': args.location,
                'file': args.filenames,
                'currency': args.currency,
                'host': args.host
            }
            serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
            #d = _Orchestrate()
            #d.copy_file()
            #db_present = d.check_for_db()
            #if db_present:
            #    create_management_db()
            load_db(file=args.filenames, location=args.location)
            launch_report_server(location=args.location, port=args.port, host=args.host)
        except OSError as e:
            print(e)

    elif args.location and args.launch_console and args.port and args.host:
        # -loc -lx -p --host
        try:
            print(6)

            app_settings = {
                'database_path': args.location,
                'host': args.host,
                'currency': args.currency,
                'file': args.filenames
            }
            serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
            launch_report_server(location=args.location, port=args.port, host=args.host)
        except OSError as e:
            print(e)

    elif args.analyse_file and args.location is not None and args.filenames is not None and args.launch_console is None and args.host:
        # -a -loc -lx --host
        print(7)

        app_settings = {
            'database_path': args.location,
            'host': args.host,
            'currency': args.currency
        }
        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
        launch_report_server(location=args.location, port=args.port, host=args.host)

    elif args.chat:
        msg = input("Enter message for Dash: ")
        while msg != 'q':
            dash = ChatBot()
            response = dash.chat_machine(message=msg)
            for i in response:
                print('Dash> ', i)
            msg = input("> ")
    else:
        launch_report()

if __name__ == '__main__':
    main()
