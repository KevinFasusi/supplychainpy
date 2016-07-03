#!/usr/bin/env python

import argparse

from supplychainpy.launch_reports import launch_report

from supplychainpy.reporting import load
from supplychainpy.reporting.views import db, app


def main():
    parser = argparse.ArgumentParser(description='Supplychainpy commandline interface a')

    parser.add_argument(dest='filenames', metavar='filename', nargs='?')

    parser.add_argument('-l', '--lau', dest='launch', action='store_true',
                        help='launch supplychainpy reporting')

    parser.add_argument('-p', dest='process', action='store_true',
                        help='process file and perform analysis/')

    parser.add_argument('-o', dest='outfile', action='store',
                        help='output file')

    args = parser.parse_args()

    if args.launch == True and args.process == True and args.filenames is not None:
        db.create_all()
        load.load(args.filenames)
        launch_report()

    elif args.launch == True:
        launch_report()


if __name__ == '__main__':
    main()
