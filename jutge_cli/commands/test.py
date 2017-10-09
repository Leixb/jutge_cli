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

from glob import glob
from logging import getLogger
from os.path import expanduser, basename
from subprocess import Popen, PIPE, check_output, CalledProcessError
from tempfile import NamedTemporaryFile

from . import download
from . import get_code

log = getLogger('jutge.test')

class global_vars:

    quiet, no_colors = False, False

ansi_colors = dict(
    HEADER = '\033[95m',
    BLUE = '\033[94m',
    GREEN = '\033[92m',
    WARNING = '\033[93m',
    FAIL = '\033[91m',
    BOLD = '\033[1m',
    UNDERLINE = '\033[4m',
    ENDC = '\033[0m')

def print_color(text, colors=None):
    if not global_vars.quiet:
        if colors == None or global_vars.no_colors:
            print(text)
            return
        elif not isinstance(colors,list):
            colors = [colors]
        for color in colors:
            print(ansi_colors[color],end='')
        print(text)
        for color in colors:
            print(ansi_colors['ENDC'],end='')

class test:

    def __init__(self, args):
        self.args = args
        global_vars.no_colors = self.args.no_color
        log.debug('No colors' + str(global_vars.no_colors))
        if args.SUBCOMMAND == 'test':
            global_vars.quiet = self.args.quiet
            exit(self.eval())
        global_vars.quiet = True

    def eval(self):

        if isinstance(self.args.prog, str):
            source_file = self.args.prog
        else:
            source_file = self.args.prog.name

        if source_file.endswith('.cpp') or source_file.endswith('.cc'):

            prog_name = '.'.join(source_file.split('.')[:-1]) + '.x'
            log.debug('Compiling to {}'.format(prog_name))

            p = Popen(
                    ['g++', '-std=c++11', '-g', source_file, '-o', prog_name])
            return_code = p.wait()

            if return_code:
                log.error('Compilation returned {}'.format(return_code))
                exit(return_code)

        else: prog_name = source_file

        if not prog_name[0] in ('.','/'):
            prog_name = './' + prog_name

        cont, cor = 0, 0

        code = get_code.get_code(self.args).code
        download.download(self.args)

        for sample_inp in sorted(glob(
                    '{}/{}/*.{}'.format(expanduser(self.args.database),
                    code,
                    self.args.inp_suffix))):
            sample_cor = ''.join(sample_inp.split('.')[:-1]) \
                    + '.' + self.args.cor_suffix

            try:
                test_input = open(sample_inp, 'r')
                test_output = NamedTemporaryFile()

                header_text = '*** Input ' + str(cont) + ' '

                if basename(sample_inp).startswith('custom'):
                    if self.args.no_custom:
                        continue
                    header_text += '(custom) '

                cont += 1

                p = Popen(
                        prog_name, stdin=test_input, stdout=test_output,
                        stderr=PIPE)
                return_code = p.wait()

                if return_code:
                    log.warning('Program exited with code: ' + return_code)

                test_input.seek(0)

                print_color('{:*<79}'.format(header_text), ['BLUE', 'BOLD'])
                print_color(test_input.read(), 'HEADER')
            finally:
                test_input.close()

            try:
                out  = check_output(
                        [self.args.diff_prog]\
                        + self.args.diff_flags.split(',')\
                        + [test_output.name, sample_cor]
                        )
                print_color('{:*<79}'.format('*** OK '),['GREEN', 'BOLD'])
                print_color(out.decode('UTF-8'))

                cor+=1

            except CalledProcessError as err:   # Thrown if files doesn't match
                print_color( '{:*<79}'.format('*** WA '), ['BOLD', 'FAIL'])
                print_color(err.output.decode('UTF-8'))
            finally:
                test_output.close()

        result = ' ({:02}/{:02})'.format(cor,cont)
        if cont == 0:
            print_color('Program has no test-cases yet')
        elif cont == cor:
            print_color(
                    '{:*^79}'.format(result + ' ALL OK :) '), ['GREEN', 'BOLD']
                    )
        else:
            print_color('{:*^79}'.format(result + ' :( '), ['FAIL', 'BOLD'])

        return cont-cor

