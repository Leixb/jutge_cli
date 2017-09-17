#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jadd_cases')

from os.path import isdir
from os import mkdir
from glob import glob

class jadd_cases:
    def __init__(self,args):
        if args.input_file == sys.stdin: print('Enter input:')
        src_inp = args.input_file.read()
        if args.output_file == sys.stdin: print('Enter output:')
        src_cor = args.output_file.read()

        code = getcode(args)

        dest_folder = '{}/{}'.format(args.database,code)
        if not isdir(dest_folder): mkdir(dest_folder)

        files = glob('{}/custom-*',dest_folder)
        if files: n = basename(files).split('-','.')[-1]+1
        else: n = 0

        dest = '{}/custom-{}'.format(dest_folder,n)

        open('{}.{}'.format(dest,args.inp_suffix)).write(src_inp)
        open('{}.{}'.format(dest,args.cor_suffix)).write(src_cor)

