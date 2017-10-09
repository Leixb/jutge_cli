#!/usr/bin/python3

# Copyright (C) 2017  Aleix Boné (abone9999 at gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import logging

import argparse

try:
    from .commands import *
except ModuleNotFoundError:
    from commands import *

JUTGE_CLI_VERSION = '1.6.3'

CONFIG = defaults.config()['param']

BANNER = '''\

       ██╗██╗   ██╗████████╗ ██████╗ ███████╗   ______     ___
       ██║██║   ██║╚══██╔══╝██╔════╝ ██╔════╝  / ___| |   |_ _|
       ██║██║   ██║   ██║   ██║  ███╗█████╗   | |   | |    | |
  ██   ██║██║   ██║   ██║   ██║   ██║██╔══╝   | |___| |___ | |
  ╚█████╔╝╚██████╔╝   ██║   ╚██████╔╝███████╗  \____|_____|___|
   ╚════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝  v{} by Leix_b

'''.format(JUTGE_CLI_VERSION)

PARSER = argparse.ArgumentParser(
    description=BANNER,
    formatter_class=argparse.RawDescriptionHelpFormatter)

PARENT_PARSER = argparse.ArgumentParser(add_help=False)

PARENT_PARSER.add_argument('-d', '--database', type=str,
        default=CONFIG['database'],
        help='directory containing the test samples')
PARENT_PARSER.add_argument('-r', '--regex', type=str,
        help='regular expression used to find the code from filename',
        default=CONFIG['regex'])
PARENT_PARSER.add_argument('--no-download', action='store_true', default=False,
        help='do not attempt to fetch data from jutge.org')
PARENT_PARSER.add_argument('--cookie', type=str,
        metavar='PHPSESSID',
        help='cookie used to fetch data from jutge.org (this is needed for private problems which code begins with an X)')

PARENT_PARSER_VERBOSITY = PARENT_PARSER.add_mutually_exclusive_group()
PARENT_PARSER_VERBOSITY.add_argument('-q', '--quiet', action='store_true')
PARENT_PARSER_VERBOSITY.add_argument('-v', '--verbosity', action='count',
        default=0)

SUBPARSERS = PARSER.add_subparsers(title='subcommands', dest='SUBCOMMAND')
SUBPARSERS.required = True

PARSER_ADD_TEST = SUBPARSERS.add_parser('add-test', aliases=['add'],
        help='add custom test case to database',
        parents=[PARENT_PARSER])
PARSER_ADD_TEST.set_defaults(subcommand=add_test.add_test)
PARSER_ADD_TEST_CODE = PARSER_ADD_TEST.add_mutually_exclusive_group(
        required=True)
PARSER_ADD_TEST_CODE.add_argument('-p', '--prog', type=argparse.FileType('r'),
        metavar='prog.cpp',
        help='program to test')
PARSER_ADD_TEST_CODE.add_argument('-c', '--code', type=str,
        help='code to use instead of searching in the filename')
PARSER_ADD_TEST.add_argument('-i', '--input-file', type=argparse.FileType('r'),
        metavar='test1.inp',
        help='test case input file',
        default=sys.stdin)
PARSER_ADD_TEST.add_argument('-o', '--output-file', type=argparse.FileType('r'),
        metavar='test1.cor',
        help='test case expected output file',
        default=sys.stdin)
PARSER_ADD_TEST.add_argument('--inp-suffix', type=str,
        default=CONFIG['inp-suffix'],
        help='suffix of test input files')
PARSER_ADD_TEST.add_argument('--cor-suffix', type=str,
        default=CONFIG['cor-suffix'],
        help='suffix of test correct output files')
PARSER_ADD_TEST.add_argument('--delete', action='store_true', default=False,
        help='delete all custom tests for problem')

PARSER_ARCHIVE = SUBPARSERS.add_parser('archive', aliases=['done'],
        help='move program to archived folder',
        parents=[PARENT_PARSER])
PARSER_ARCHIVE.set_defaults(subcommand=archive.archive)
PARSER_ARCHIVE.add_argument('prog', type=argparse.FileType('r+'),
        metavar='prog.cpp',
        help='file to move')
PARSER_ARCHIVE.add_argument('-f', '--folder', type=str,
        default=CONFIG['folder'],
        help='folder where program will be archived')
PARSER_ARCHIVE.add_argument('--overwrite', action='store_true', default=False,
        help='overwrite program if already in archive')
PARSER_ARCHIVE.add_argument('--no-delete', action='store_true', default=False,
        help='do not delete file after archiving')

PARSER_CHECK_SUBMISSIONS = SUBPARSERS.add_parser('check-submissions',
        aliases=['check'],
        help='check last sent submissions',
        parents=[PARENT_PARSER])
PARSER_CHECK_SUBMISSIONS.set_defaults(subcommand=check_submissions.check_submissions)
PARSER_CHECK_SUBMISSIONS_MODE = \
        PARSER_CHECK_SUBMISSIONS.add_mutually_exclusive_group()
PARSER_CHECK_SUBMISSIONS_MODE.add_argument('--last', action='store_true',
        default=False,
        help='only show last submission')
PARSER_CHECK_SUBMISSIONS_MODE.add_argument('--reverse', action='store_true',
        help='show last submission on top',
        default=False)
PARSER_CHECK_SUBMISSIONS_MEX = \
        PARSER_CHECK_SUBMISSIONS.add_mutually_exclusive_group()
PARSER_CHECK_SUBMISSIONS_MEX.add_argument('-p', '--prog',
        type=argparse.FileType('r'),
        metavar='prog.cpp',
        help='filename from which we can extract the problem code')
PARSER_CHECK_SUBMISSIONS_MEX.add_argument('-c', '--code', type=str,
        help='problem code')

PARSER_COOKIE = SUBPARSERS.add_parser('cookie',
        help='save cookie to temporary file for later use to delete cookie \
                issue the command: jutge cookie delete',
        parents=[PARENT_PARSER])
PARSER_COOKIE.set_defaults(subcommand=cookie.cookie)
PARSER_COOKIE.add_argument('cookie',
        metavar='PHPSESSID',
        help='cookie to save (special values: delete -> deletes saved cookie; \
                print -> print current saved cookie)')
PARSER_COOKIE.add_argument('--skip-check', action='store_true', default=False,
        help='Save cookie file even if not valid')

PARSER_DOWNLOAD = SUBPARSERS.add_parser('download', aliases=['down'],
        help='download problem files to local database',
        parents=[PARENT_PARSER])
PARSER_DOWNLOAD.set_defaults(subcommand=download.download)
PARSER_DOWNLOAD_MEX = PARSER_DOWNLOAD.add_mutually_exclusive_group(
        required=True)
PARSER_DOWNLOAD_MEX.add_argument('-p', '--prog', type=argparse.FileType('r'),
        metavar='prog.cpp',
        help='filename from which we can extract the problem code')
PARSER_DOWNLOAD_MEX.add_argument('-c', '--code', type=str,
        help='problem code')
PARSER_DOWNLOAD.add_argument('--overwrite', action='store_true', default=False,
        help='overwrite existing files in database')

PARSER_LOGIN = SUBPARSERS.add_parser('login', parents=[PARENT_PARSER],
        help='login to jutge.org and save cookie')
PARSER_LOGIN.set_defaults(subcommand=login.login)
PARSER_LOGIN.add_argument('--email', default=CONFIG['email'],
        help='jutge.org email')
PARSER_LOGIN.add_argument('--password', default=CONFIG['password'],
        help='jutge.org password')

PARSER_NEW = SUBPARSERS.add_parser('new', aliases=['create'],
        help='create new file',
        parents=[PARENT_PARSER])
PARSER_NEW.set_defaults(subcommand=new.new)
PARSER_NEW.add_argument('code', type=str,
        help='problem code')
PARSER_NEW.add_argument('-t', '--type', type=str, default='cpp',
        help='file extension')
PARSER_NEW.add_argument('--overwrite',
        action='store_true',
        help='overwrite existing files',
        default=False)
PARSER_NEW.add_argument('--problem-set',
        action='store_true',
        help='Create all files in problem set',
        default=False)

PARSER_SHOW = SUBPARSERS.add_parser('show', aliases=['print'],
        help='show title, statement or test cases corresponding to problem \
                code',
        parents=[PARENT_PARSER])
PARSER_SHOW.set_defaults(subcommand=show.show)
PARSER_SHOW.add_argument('mode',
        type=str,
        choices=['title', 'stat', 'cases'])
PARSER_SHOW_CODE = PARSER_SHOW.add_mutually_exclusive_group(required=True)
PARSER_SHOW_CODE.add_argument('-p', '--prog',
        metavar='prog.cpp',
        type=argparse.FileType('r'),
        help='filename from which we can extract the problem code')
PARSER_SHOW_CODE.add_argument('-c', '--code',
        type=str,
        help='problem code to use')
PARSER_SHOW.add_argument('--inp-suffix',
        type=str,
        help='suffix of test input files',
        default=CONFIG['inp-suffix'])
PARSER_SHOW.add_argument('--cor-suffix', type=str,
        default=CONFIG['cor-suffix'],
        help='suffix of test correct output files')

PARSER_TEST = SUBPARSERS.add_parser('test',
        help='test program using cases from database',
        parents=[PARENT_PARSER])
PARSER_TEST.set_defaults(subcommand=test.test)
PARSER_TEST.add_argument('prog', type=argparse.FileType('r'),
        metavar='prog.cpp',
        help='Program to test')
PARSER_TEST.add_argument('-c', '--code', type=str,
        help='code to use instead of searching in the filename')
PARSER_TEST.add_argument('--diff-prog', type=str, default=CONFIG['diff-prog'],
        help='diff shell command to compare tests')
PARSER_TEST.add_argument('--diff-flags', type=str,
        default=CONFIG['diff-flags'],
        help='diff shell command flags used to compare tests \
                (comma separated)')
PARSER_TEST.add_argument('--inp-suffix', type=str,
        default=CONFIG['inp-suffix'],
        help='suffix of test input files')
PARSER_TEST.add_argument('--cor-suffix', type=str,
        default=CONFIG['cor-suffix'],
        help='suffix of test correct output files')
PARSER_TEST.add_argument('--no-custom', action='store_true', default=False,
        help='do not test custom cases')
PARSER_TEST.add_argument('--no-color', action='store_true', default=False,
        help='do not use ansi color sequences')

PARSER_UPDATE = SUBPARSERS.add_parser('update', aliases=['import'],
        help='add programs to archived folder from zip file',
        parents=[PARENT_PARSER])
PARSER_UPDATE.set_defaults(subcommand=update.update)
PARSER_UPDATE.add_argument('zip', type=argparse.FileType('r'),
        help='zip file containing the problems')
PARSER_UPDATE.add_argument('-f', '--folder', type=str,
        default=CONFIG['folder'],
        help='archive folder')
PARSER_UPDATE.add_argument('--delay', type=int, default=100,
        metavar='milliseconds',
        help='delay between jutge.org GET requests')
PARSER_UPDATE.add_argument('--overwrite', action='store_true', default=False,
        help='overwrite programs already found in archive')

PARSER_UPLOAD = SUBPARSERS.add_parser('upload', aliases=['up'],
        help='Upload program for jutge evaluation',
        parents=[PARENT_PARSER])
PARSER_UPLOAD.set_defaults(subcommand=upload.upload)
PARSER_UPLOAD.add_argument('prog', type=str,
        metavar='prog.cpp',
        help='program file to upload')
PARSER_UPLOAD.add_argument('-c', '--code', type=str,
        metavar='CODE',
        help='code of problem to submit')
PARSER_UPLOAD.add_argument('--compiler', type=str,
        metavar='COMPILER_ID',
        help='jutge.org compiler_id to use')
PARSER_UPLOAD.add_argument('--problem-set', action='store_true', default=False,
        help='upload all files in problem set')
PARSER_UPLOAD.add_argument('--delay', type=int, default=100,
        metavar='milliseconds',
        help='delay between jutge.org upload requests')
PARSER_UPLOAD.add_argument('-f', '--folder', type=str,
        default=CONFIG['folder'],
        help='folder where programs are archived')
PARSER_UPLOAD.add_argument('--skip-test', action='store_true', default=False,
        help='do not test public cases before uploading')
PARSER_UPLOAD.add_argument('--no-skip-accepted', action='store_true',
        default=False,
        help='do not skip accepted problems when uploading')
PARSER_UPLOAD.add_argument('--check', action='store_true', default=False,
        help='wait for veredict after uploading')

def main():
    args = PARSER.parse_args()

    global DATABASE, REGEX, NO_DOWNLOAD, COOKIE

    DATABASE = args.database
    REGEX = args.regex
    NO_DOWNLOAD = args.no_download
    COOKIE = args.cookie

    if args.verbosity >= 3:
        log_lvl = logging.DEBUG
    elif args.verbosity == 2:
        log_lvl = logging.INFO
    elif args.verbosity == 1:
        log_lvl = logging.WARNING
    elif args.quiet:
        log_lvl = logging.CRITICAL
    else:
        log_lvl = logging.ERROR

    logging.basicConfig(
            format='%(name)s; %(levelname)s: %(message)s', level=log_lvl)
    log = logging.getLogger('jutge')

    log.debug(args.regex)
    log.debug(args.database)

    # Add code to kwargs
    args_dict = vars(args)
    args_dict['code'] = get_code.get_code(args).code

    args.subcommand(**args_dict)  #expand flags to kwargs


if __name__ == '__main__':
    main()

