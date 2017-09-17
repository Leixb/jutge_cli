#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jadd_cases')

from os.path import isdir, expanduser,basename
from os import mkdir,remove
from glob import glob
import sys

import re

import jgetcode

class jadd_cases:
    def __init__(self,args):

        code = jgetcode.jgetcode(args).code
        dest_folder = expanduser('{}/{}'.format(args.database,code))

        if args.delete:
            for custom_test in glob('{}/custom-*'.format(dest_folder)):
                remove(custom_test)
            return

        if args.input_file == sys.stdin: print('Enter input:')
        src_inp = args.input_file.read()
        if args.output_file == sys.stdin: print('Enter output:')
        src_cor = args.output_file.read()

        if not isdir(dest_folder): mkdir(dest_folder)

        files = sorted(glob('{}/custom-*'.format(dest_folder)))
        if files: n = int(re.search('-([0-9]*).',basename(files[-1])).group(1))+1
        else: n = 0

        dest = '{}/custom-{}'.format(dest_folder,n)

        open('{}.{}'.format(dest,args.inp_suffix),'a').write(src_inp)
        open('{}.{}'.format(dest,args.cor_suffix),'a').write(src_cor)

