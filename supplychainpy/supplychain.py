#!/usr/bin/env python

import argparse

import sys

from supplychainpy.launch_reports import launch_load_report, launch_report, load_db


def main():
    parser = argparse.ArgumentParser(description='Supplychainpy commandline interface a')

    parser.add_argument(dest='filenames', metavar='filename', nargs='?')

    parser.add_argument('-l', '--lau', dest='launch', action='store_true',
                        help='launch supplychainpy reporting')

    parser.add_argument('-p', dest='process', action='store_true',
                        help='process file and perform analysis/')

    parser.add_argument('-o', dest='outfile', action='store',
                        help='output file')

    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose mode')

    parser.add_argument('-db', dest='database', action='store',
                        help='database engine uri e.g. ')

    parser.add_argument('-loc', dest='location', action='store',
                        help='database path e.g. ')

    args = parser.parse_args()

    if args.verbose:
        print('filenames = {}'.format(args.filenames))
        print('launch reports = {}'.format(args.launch))
        print('process file = {}'.format(args.process))
        print('database location = {}'.format(args.location))

    if args.launch and args.process and args.filenames is not None and args.location is None:
        print(1)
        launch_load_report(args.filenames)

    elif args.launch and args.process and args.filenames is not None and args.location is not None:
        print(2)
        launch_load_report(args.filenames, args.location)

    elif args.launch and args.location is not None:
        print(3)
        launch_report(location=args.location)

    elif args.process and args.location is not None and args.filenames is not None:
        print(4)
        load_db(file=args.filenames, location=args.location)

    if args.filenames is None and False == args.process and False == args.launch and args.outfile is None:
        filename = input('path to "CSV" or "text" file... ')
        sys.stdout.flush()


if __name__ == '__main__':
    main()
