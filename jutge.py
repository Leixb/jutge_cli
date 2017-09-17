#!/usr/bin/python3

import sys

def test(args):
    import jtest
    jtest.jtest(args)
def add_cases(args):
    import jadd_cases
    jadd_cases.jadd_cases(args)
def jprint(args):
    import jprint
    jprint.jprint(args)
def archive(args):
    import jarchive
    jarchive.jarchive(args)
def upload(args):
    import jupload
    jupload.jupload(args)
def update(args):
    import jupdate
    jupdate.jupdate(args)
def new(args):
    import jnew
    jnew.jnew(args)

import argparse

parser = argparse.ArgumentParser(prog='jutge')

parser.add_argument('-d','--database', type=str, help='Comma separated directories containing the test samples', default='~/Documents/Universitat/PROG/DB')
parser.add_argument('-r','--regex',type=str, help='Regex used to find the code from filename', default='[PGQX][0-9]{5}')
parser.add_argument('--no-download', action='store_true', help='Do not attempt to fetch data from jutge.org')
parser.add_argument('--cookie', metavar='PHPSESSID', type=str, help='Cookie used to fetch data from jutge.org')

parser_verbosity = parser.add_mutually_exclusive_group()
parser_verbosity.add_argument('-q','--quiet', action='store_true')
parser_verbosity.add_argument('-v','--verbosity', action='count')

subparsers = parser.add_subparsers(dest='cmd')
subparsers.required = True

parser_test = subparsers.add_parser('test', help='Test program using cases from database')
parser_test.add_argument('program',metavar='prog.cpp',type=argparse.FileType('rx'), help='Program to test')
parser_test.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_test.add_argument('--diff-prog', type=str, help='Diff shell command to compare tests', default='colordiff')
parser_test.add_argument('--diff-flags', type=str, help='Diff shell command flags used to compare tests (comma separated)', default='-y')
parser_test.add_argument('--inp-suffix', type=str, help='Suffix of test input files', default='inp')
parser_test.add_argument('--cor-suffix', type=str, help='Suffix of test correct output files', default='cor')
parser_test.add_argument('--no-custom', action='store_true', help='Suffix of test correct output files')
parser_test.set_defaults(func=test)

parser_add_cases = subparsers.add_parser('add-cases', help='Add custom test-cases in database')
parser_add_cases_code = parser_add_cases.add_mutually_exclusive_group(required=True)
parser_add_cases_code.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('rx'), help='Program to test')
parser_add_cases_code.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_add_cases.add_argument('-i','--input-file', metavar='test1.inp', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
parser_add_cases.add_argument('-o','--output-file', metavar='test1.cor', type=argparse.FileType('r'), help='Expected output file', default=sys.stdin)
parser_add_cases.add_argument('--inp-suffix', type=str, help='Suffix of test input files', default='inp')
parser_add_cases.add_argument('--cor-suffix', type=str, help='Suffix of test correct output files', default='cor')
parser_add_cases.set_defaults(func=add_cases)

parser_print = subparsers.add_parser('print', help='Print title,statement or public cases corresponding to problem code')
parser_print.add_argument('mode',type=str, choices=['title','stat','cases'])
parser_print = parser_print.add_mutually_exclusive_group(required=True)
parser_print.add_argument('-p','--prog',metavar='prog.cpp',type=argparse.FileType('rx'), help='Program to test')
parser_print.add_argument('-c','--code', type=str, help='Code to use instead of searching in the filename')
parser_print.set_defaults(func=jprint)

parser_archive = subparsers.add_parser('archive', help='Move program to archived folder')
parser_archive.add_argument('program',metavar='prog.cpp',type=argparse.FileType('rw'),help='File to move')
parser_archive.add_argument('-f','--folder', type=str, help='Archived folder',default='~/Documents/Universitat/PROG/Done')
parser_archive.set_defaults(func=archive)

parser_upload = subparsers.add_parser('upload', help='Upload program for jutge evaluation')
parser_upload.add_argument('program',metavar='prog.cpp',type=argparse.FileType('r'),help='File to upload')
parser_upload.set_defaults(func=upload)

parser_update = subparsers.add_parser('update', help='Add programs to Archived folder fom zip file')
parser_update.add_argument('zip', type=argparse.FileType('r'), help='Zip file containing the problems')
parser_update.add_argument('-f','--folder', type=str, help='Archived folder',default='~/Documents/Universitat/PROG/Done')
parser_update.add_argument('--delay', type=int, metavar='milliseconds', default=100)
parser_update.add_argument('--overwrite',action='store_true')
parser_update.set_defaults(func=update)

parser_new = subparsers.add_parser('new', help='Create new file')
parser_new.add_argument('code', type=str, help='Problem code')
parser_new.add_argument('-t' '--type', type=str, help='Extension', default='cpp')
parser_new.set_defaults(func=new)

args = parser.parse_args()
args.func(args)
