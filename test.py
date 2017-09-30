#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.test')

from glob import glob
from os.path import expanduser, basename
from subprocess import Popen, PIPE, check_output,CalledProcessError

from tempfile import NamedTemporaryFile

import get_code
import download

class ansi:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

class test:
    def __init__(self,args):
        if args.prog.name.endswith('.cpp') or args.prog.name.endswith('.cc'):

            prog_name = '.'.join(args.prog.name.split('.')[:-1]) + '.x'
            log.debug('Compiling to {}'.format(prog_name))

            p = Popen(['g++', '-std=c++11', '-g', args.prog.name, '-o', prog_name])
            return_code = p.wait()

            if return_code: 
                log.error('Compilation returned {}, aborting'.format(return_code))
                exit(return_code)

        else: prog_name = args.prog.name

        if prog_name[0]!='.' and prog_name[0]!='/': prog_name = './' + prog_name

        cont,cor = 0,0

        code = get_code.get_code(args).code
        download.download(args)

        for sample_inp in sorted(glob('{}/{}/*.{}'.format(expanduser(args.database),code,args.inp_suffix))):
            sample_cor = ''.join(sample_inp.split('.')[:-1]) + '.' + args.cor_suffix

            test_input = open(sample_inp,'r')
            test_output = NamedTemporaryFile()

            if basename(sample_inp).startswith('custom'):
                if args.no_custom: continue
                is_custom = '(custom)'
            else: is_custom = ''

            cont += 1

            p = Popen(prog_name, stdin=test_input,stdout=test_output,stderr=PIPE)
            return_code = p.wait()

            if return_code: log.warning("Program returned {}".format(return_code))

            test_input.seek(0)
            print(ansi.OKBLUE, ansi.BOLD, '*** Input {} {}'.format(cont,is_custom), ansi.ENDC, ansi.HEADER)
            print(test_input.read(), ansi.ENDC)
            test_input.close()

            try:
                out  = check_output([args.diff_prog]+args.diff_flags.split(',')+[test_output.name,sample_cor])
                print(ansi.OKGREEN, ansi.BOLD, '*** The results match :)', ansi.ENDC, ansi.ENDC)
                print(out.decode('UTF-8'))

                cor+=1

            except CalledProcessError as err:   # Thrown if files doesn't match
                print(ansi.FAIL, ansi.BOLD, '*** The results do NOT match :(', ansi.ENDC, ansi.ENDC)
                print(err.output.decode('UTF-8'))

            test_output.close()
        if cont == 0: print("Program has no test-cases yet")
        elif cont == cor: 
            print(ansi.OKGREEN, ansi.BOLD, '*** ({}/{}) ALL OK :)'.format(cor,cont), ansi.ENDC, ansi.ENDC)
        else:
            print(ansi.FAIL, ansi.BOLD, '*** ({}/{}) :('.format(cor,cont), ansi.ENDC, ansi.ENDC)
        exit(cont-cor)

