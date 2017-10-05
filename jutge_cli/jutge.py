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

try: from .commands import *
except ModuleNotFoundError: from commands import *

def run_test(args): test.test(args)
def run_add_test(args): add_test.add_test(args)
def run_show(args): show.show(args)
def run_archive(args): archive.archive(args)
def run_upload(args): upload.upload(args)
def run_update(args): update.update(args)
def run_new(args): new.new(args)
def run_download(args): download.download(args)
def run_cookie(args): cookie.cookie(args)
def run_check_submissions(args): check_submissions.check_submissions(args)

import argparse

jutge_cli_version = '1.4.0'

config = defaults.config().param

parser = argparse.ArgumentParser(prog='jutge',
        description='''\

       ██╗██╗   ██╗████████╗ ██████╗ ███████╗   ______     ___
       ██║██║   ██║╚══██╔══╝██╔════╝ ██╔════╝  / ___| |   |_ _|
       ██║██║   ██║   ██║   ██║  ███╗█████╗   | |   | |    | | 
  ██   ██║██║   ██║   ██║   ██║   ██║██╔══╝   | |___| |___ | | 
  ╚█████╔╝╚██████╔╝   ██║   ╚██████╔╝███████╗  \____|_____|___|
   ╚════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝  v{} by Leix_b

'''.format(jutge_cli_version),
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

parent_parser = argparse.ArgumentParser(add_help=False)

parent_parser.add_argument('-d','--database', type=str, help='directory containing the test samples', default=config['database'])
parent_parser.add_argument('-r','--regex',type=str, help='regular expression used to find the code from filename', default=config['regex'])
parent_parser.add_argument('--no-download', action='store_true', help='do not attempt to fetch data from jutge.org', default=False)
parent_parser.add_argument('--cookie', metavar='PHPSESSID', type=str, help='cookie used to fetch data from jutge.org (this is needed for private problems which code begins with an X)')

parent_parser_verbosity = parent_parser.add_mutually_exclusive_group()
parent_parser_verbosity.add_argument('-q','--quiet', action='store_true')
parent_parser_verbosity.add_argument('-v','--verbosity', action='count', default=0)

subparsers = parser.add_subparsers(title='subcommands', dest='SUBCOMMAND')
subparsers.required = True

parser_test = subparsers.add_parser('test', help='test program using cases from database', parents=[parent_parser])
parser_test.add_argument('prog',metavar='prog.cpp',type=argparse.FileType('r'), help='Program to test')
parser_test.add_argument('-c','--code', type=str, help='code to use instead of searching in the filename')
parser_test.add_argument('--diff-prog', type=str, help='diff shell command to compare tests', default=config['diff-prog'])
parser_test.add_argument('--diff-flags', type=str, help='diff shell command flags used to compare tests (comma separated)', default=config['diff-flags'])
parser_test.add_argument('--inp-suffix', type=str, help='suffix of test input files', default=config['inp-suffix'])
parser_test.add_argument('--cor-suffix', type=str, help='suffix of test correct output files', default=config['cor-suffix'])
parser_test.add_argument('--no-custom', action='store_true', help='do not test custom cases', default=False)
parser_test.set_defaults(func=run_test)

parser_add_test = subparsers.add_parser('add-test', aliases=['add'], help='add custom test case to database', parents=[parent_parser])
parser_add_test_code = parser_add_test.add_mutually_exclusive_group(required=True)
parser_add_test_code.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='program to test')
parser_add_test_code.add_argument('-c','--code', type=str, help='code to use instead of searching in the filename')
parser_add_test.add_argument('-i','--input-file', metavar='test1.inp', type=argparse.FileType('r'), help='test case input file', default=sys.stdin)
parser_add_test.add_argument('-o','--output-file', metavar='test1.cor', type=argparse.FileType('r'), help='test case expected output file', default=sys.stdin)
parser_add_test.add_argument('--inp-suffix', type=str, help='suffix of test input files', default=config['inp-suffix'])
parser_add_test.add_argument('--cor-suffix', type=str, help='suffix of test correct output files', default=config['cor-suffix'])
parser_add_test.add_argument('--delete', action='store_true', help='delete all custom tests for problem', default=False)
parser_add_test.set_defaults(func=run_add_test)

parser_show = subparsers.add_parser('show', aliases=['print'], help='show title, statement or test cases corresponding to problem code', parents=[parent_parser])
parser_show.add_argument('mode',type=str, choices=['title','stat','cases'])
parser_show_code = parser_show.add_mutually_exclusive_group(required=True)
parser_show_code.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='filename from which we can extract the problem code')
parser_show_code.add_argument('-c','--code', type=str, help='problem code to use')
parser_show.add_argument('--inp-suffix', type=str, help='suffix of test input files', default=config['inp-suffix'])
parser_show.add_argument('--cor-suffix', type=str, help='suffix of test correct output files', default=config['cor-suffix'])
parser_show.set_defaults(func=run_show)

parser_archive = subparsers.add_parser('archive', aliases=['done'], help='move program to archived folder', parents=[parent_parser])
parser_archive.add_argument('prog',metavar='prog.cpp',type=argparse.FileType('r+'),help='file to move')
parser_archive.add_argument('-f','--folder', type=str, help='folder where program will be archived',default=config['folder'])
parser_archive.add_argument('--overwrite',action='store_true',help='overwrite program if already in archive', default=False)
parser_archive.add_argument('--no-delete',action='store_true',help='do not delete file after archiving', default=False)
parser_archive.set_defaults(func=run_archive)

parser_upload = subparsers.add_parser('upload', aliases=['up'], help='Upload program for jutge evaluation', parents=[parent_parser])
parser_upload.add_argument('prog',metavar='prog.cpp',type=str ,help='program file to upload')
parser_upload.add_argument('-c','--code',metavar='CODE',type=str ,help='code of problem to submit')
parser_upload.add_argument('--compiler',metavar='COMPILER_ID',type=str ,help='jutge.org compiler_id to use')
parser_upload.add_argument('--problem-set',action='store_true', help='upload all files in problem set', default=False)
parser_upload.add_argument('--delay', type=int, metavar='milliseconds', help='delay between jutge.org upload requests', default=100)
parser_upload.add_argument('-f','--folder', type=str, help='folder where programs are archived',default=config['folder'])
parser_upload.set_defaults(func=run_upload)

parser_update = subparsers.add_parser('update', aliases=['import'], help='add programs to archived folder from zip file', parents=[parent_parser])
parser_update.add_argument('zip', type=argparse.FileType('r'), help='zip file containing the problems')
parser_update.add_argument('-f','--folder', type=str, help='archive folder',default=config['folder'])
parser_update.add_argument('--delay', type=int, metavar='milliseconds', help='delay between jutge.org GET requests', default=100)
parser_update.add_argument('--overwrite',action='store_true', help='overwrite programs already found in archive', default=False)
parser_update.set_defaults(func=run_update)

parser_new = subparsers.add_parser('new', aliases=['create'], help='create new file', parents=[parent_parser])
parser_new.add_argument('code', type=str, help='problem code')
parser_new.add_argument('-t', '--type', type=str, help='file extension', default='cpp')
parser_new.add_argument('--overwrite',action='store_true', help='overwrite existing files', default=False)
parser_new.add_argument('--problem-set',action='store_true', help='Create all files in problem set', default=False)
parser_new.set_defaults(func=run_new)

parser_download = subparsers.add_parser('download', aliases=['down'], help='download problem files to local database', parents=[parent_parser])
parser_download_mex = parser_download.add_mutually_exclusive_group(required=True)
parser_download_mex.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='filename from which we can extract the problem code')
parser_download_mex.add_argument('-c','--code', type=str, help='problem code')
parser_download.add_argument('--overwrite',action='store_true', help='overwrite existing files in database', default=False)
parser_download.set_defaults(func=run_download)

parser_check_submissions = subparsers.add_parser('check-submissions', aliases=['check'], help='check last sent submissions', parents=[parent_parser])
parser_check_submissions_mode = parser_check_submissions.add_mutually_exclusive_group()
parser_check_submissions_mode.add_argument('--last', action='store_true', help='only show last submission', default=False)
parser_check_submissions_mode.add_argument('--reverse', action='store_true', help='show last submission on top', default=False)
parser_check_submissions.set_defaults(func=run_check_submissions)

parser_cookie = subparsers.add_parser('cookie', help='save cookie to temporary file for later use to delete cookie isse the command: jutge cookie delete', parents=[parent_parser])
parser_cookie.add_argument('cookie', metavar='PHPSESSID', help='cookie to save (special values: delete -> deletes saved cookie; print -> print current saved cookie)')
parser_cookie.add_argument('--skip-check', action='store_true', help='Save cookie file even if not valid', default=False)
parser_cookie.set_defaults(func=run_cookie)

def main():
    args = parser.parse_args()

    if args.verbosity >= 3: log_lvl = logging.DEBUG
    elif args.verbosity == 2: log_lvl = logging.INFO
    elif args.verbosity == 1: log_lvl = logging.WARNING
    elif args.quiet: log_lvl = logging.CRITICAL
    else: log_lvl = logging.ERROR

    logging.basicConfig(format='%(name)s; %(levelname)s: %(message)s',level=log_lvl)
    log = logging.getLogger('jutge')

    log.debug(args.regex)
    log.debug(args.database)

    args.func(args)

if __name__ == '__main__': main()

