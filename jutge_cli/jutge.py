#!/usr/bin/python3

import sys
import logging

from .commands import *

def run_test(args): test.test(args)
def run_add_test(args): add_test.add_test(args)
def run_show(args): show.show(args)
def run_archive(args): archive.archive(args)
def run_upload(args): upload.upload(args)
def run_update(args): update.update(args)
def run_new(args): new.new(args)
def run_download(args): download.download(args)
def run_cookie(args): cookie.cookie(args)

import argparse

config = defaults.config().param

parser = argparse.ArgumentParser(prog='jutge',
        description='''
     ██╗██╗   ██╗████████╗ ██████╗ ███████╗     ██████╗██╗     ██╗
     ██║██║   ██║╚══██╔══╝██╔════╝ ██╔════╝    ██╔════╝██║     ██║
     ██║██║   ██║   ██║   ██║  ███╗█████╗      ██║     ██║     ██║
██   ██║██║   ██║   ██║   ██║   ██║██╔══╝      ██║     ██║     ██║
╚█████╔╝╚██████╔╝   ██║   ╚██████╔╝███████╗    ╚██████╗███████╗██║
 ╚════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝     ╚═════╝╚══════╝╚═╝
        '''
        )

parser.add_argument('-d','--database', type=str, help='Directory containing the test samples', default=config['database'])
parser.add_argument('-r','--regex',type=str, help='Regex used to find the code from filename', default=config['regex'])
parser.add_argument('--no-download', action='store_true', help='Do not attempt to fetch data from jutge.org')
parser.add_argument('--cookie', metavar='PHPSESSID', type=str, help='Cookie used to fetch data from jutge.org')

parser_verbosity = parser.add_mutually_exclusive_group()
parser_verbosity.add_argument('-q','--quiet', action='store_true')
parser_verbosity.add_argument('-v','--verbosity', action='count', default=0)

subparsers = parser.add_subparsers(dest='cmd')
subparsers.required = True

parser_test = subparsers.add_parser('test', help='Test program using cases from database')
parser_test.add_argument('prog',metavar='prog.cpp',type=argparse.FileType('r'), help='Program to test')
parser_test.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_test.add_argument('--diff-prog', type=str, help='Diff shell command to compare tests', default=config['diff-prog'])
parser_test.add_argument('--diff-flags', type=str, help='Diff shell command flags used to compare tests (comma separated)', default=config['diff-flags'])
parser_test.add_argument('--inp-suffix', type=str, help='Suffix of test input files', default=config['inp-suffix'])
parser_test.add_argument('--cor-suffix', type=str, help='Suffix of test correct output files', default=config['cor-suffix'])
parser_test.add_argument('--no-custom', action='store_true', help='Do not test custom cases')
parser_test.set_defaults(func=run_test)

parser_add_test = subparsers.add_parser('add-test', help='Add custom test-case to database')
parser_add_test_code = parser_add_test.add_mutually_exclusive_group(required=True)
parser_add_test_code.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='Program to test')
parser_add_test_code.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_add_test.add_argument('-i','--input-file', metavar='test1.inp', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
parser_add_test.add_argument('-o','--output-file', metavar='test1.cor', type=argparse.FileType('r'), help='Expected output file', default=sys.stdin)
parser_add_test.add_argument('--inp-suffix', type=str, help='Suffix of test input files', default=config['inp-suffix'])
parser_add_test.add_argument('--cor-suffix', type=str, help='Suffix of test correct output files', default=config['cor-suffix'])
parser_add_test.add_argument('--delete', action='store_true', help='Delete all custom tests for problem', default=False)
parser_add_test.set_defaults(func=run_add_test)

parser_show = subparsers.add_parser('show', help='Show title,statement or public cases corresponding to problem code')
parser_show.add_argument('mode',type=str, choices=['title','stat','cases'])
parser_show = parser_show.add_mutually_exclusive_group(required=True)
parser_show.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='Program to test')
parser_show.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_show.add_argument('--inp-suffix', type=str, help='Suffix of test input files', default=config['inp-suffix'])
parser_show.add_argument('--cor-suffix', type=str, help='Suffix of test correct output files', default=config['cor-suffix'])
parser_show.set_defaults(func=run_show)

parser_archive = subparsers.add_parser('archive', help='Move program to archived folder')
parser_archive.add_argument('prog',metavar='prog.cpp',type=argparse.FileType('r+'),help='File to move')
parser_archive.add_argument('-f','--folder', type=str, help='Archived folder',default=config['folder'])
parser_archive.add_argument('--overwrite',action='store_true',default=False)
parser_archive.add_argument('-c','--code',type=str)
parser_archive.set_defaults(func=run_archive)

parser_upload = subparsers.add_parser('upload', help='Upload program for jutge evaluation')
parser_upload.add_argument('prog',metavar='prog.cpp',type=argparse.FileType('r'),help='File to upload')
parser_upload.set_defaults(func=run_upload)

parser_update = subparsers.add_parser('update', help='Add programs to Archived folder fom zip file')
parser_update.add_argument('zip', type=argparse.FileType('r'), help='Zip file containing the problems')
parser_update.add_argument('-f','--folder', type=str, help='Archived folder',default=config['folder'])
parser_update.add_argument('--delay', type=int, metavar='milliseconds', default=100)
parser_update.add_argument('--overwrite',action='store_true')
parser_update.set_defaults(func=run_update)

parser_new = subparsers.add_parser('new', help='Create new file')
parser_new.add_argument('code', type=str, help='Problem code')
parser_new.add_argument('-t', '--type', type=str, help='Extension', default='cpp')
parser_new.add_argument('--overwrite',action='store_true',default=False)
parser_new.set_defaults(func=run_new)

parser_download = subparsers.add_parser('download', help='Download to DB')
parser_download_mex = parser_download.add_mutually_exclusive_group(required=True)
parser_download_mex.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('r'), help='Program to test')
parser_download_mex.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_download.add_argument('--overwrite',action='store_true', default=False)
parser_download.set_defaults(func=run_download)

parser_cookie = subparsers.add_parser('cookie', help='Save cookie to tmp')
parser_cookie.add_argument('cookie', metavar='PHPSESSID')
parser_cookie.add_argument('--delete', action='store_true', default=False)
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
