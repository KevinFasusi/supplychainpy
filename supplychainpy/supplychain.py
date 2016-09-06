# Copyright (c) 2015-2016, Kevin Fasusi
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

from supplychainpy.launch_reports import launch_load_report, launch_report, load_db


def main():
    parser = argparse.ArgumentParser(description='Supplychainpy commandline interface a')

    parser.add_argument(dest='filenames', metavar='filename', nargs='?')

    parser.add_argument('-l', '--launch', dest='launch', action='store_true',
                        help='launch supplychainpy reporting')

    parser.add_argument('-a', dest='analyse_file', action='store_true',
                        help='processes file and performs analysis/')

    parser.add_argument('-o', dest='outfile', action='store',
                        help='output file')

    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose mode')

    parser.add_argument('-db', dest='database', action='store',
                        help='database engine uri e.g. ')

    parser.add_argument('-loc', dest='location', action='store',
                        help='database path e.g. ')

    parser.add_argument('-u', dest='user', action='store',
                        help='user name ')

    parser.add_argument('-p', dest='port', action='store',
                        help='port to use for local server e.g. 8080 (default: 5000) ')

    args = parser.parse_args()

    if args.verbose:
        print('filenames = {}'.format(args.filenames))
        print('launch reports = {}'.format(args.launch))
        print('process file = {}'.format(args.analyse_file))
        print('database location = {}'.format(args.location))

    if args.launch and args.analyse_file and args.filenames is not None and args.location is None:
        print(1)
        launch_load_report(args.filenames)

    elif args.launch and args.analyse_file and args.filenames is not None and args.location is not None:
        print(2)

        app_settings = {
            'database_path': args.location
        }

        serialise_response(app_settings)

        launch_load_report(args.filenames, args.location)

    elif args.launch and args.location is not None:
        print(3)
        launch_report(location=args.location)

    elif args.analyse_file and args.location is not None and args.filenames is not None:
        print(4)
        load_db(file=args.filenames, location=args.location)

    if args.filenames is None and False == args.analyse_file and False == args.launch and args.outfile is None:
        filename = input('path to "CSV" or "text" file... ')
        sys.stdout.flush()


def serialise_response(db_path: dict):
    APP_DIR = os.path.dirname(__file__, )
    REL_PATH = 'config.pickle'
    ABS_FILE_PATH = os.path.abspath(os.path.join(APP_DIR, '', REL_PATH))
    with open(ABS_FILE_PATH, 'wb') as f:
        pickle.dump(db_path, f)


if __name__ == '__main__':
    main()
