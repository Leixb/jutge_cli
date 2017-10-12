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

"""Provides function test that tests a given code or executable againt
test cases in database
"""

from glob import glob
from logging import getLogger
from os.path import basename
from subprocess import Popen, PIPE, check_output, CalledProcessError
from tempfile import NamedTemporaryFile

LOG = getLogger('jutge.test')


__ANSI_COLORS__ = dict(
    HEADER='\033[95m',
    BLUE='\033[94m',
    GREEN='\033[92m',
    WARNING='\033[93m',
    FAIL='\033[91m',
    BOLD='\033[1m',
    UNDERLINE='\033[4m',
    ENDC='\033[0m')


def test(prog, code, database, no_color=False, no_custom=False,
         inp_suffix='inp', cor_suffix='cor', diff_prog='diff',
         diff_flags='-y',
         quiet=False, **kwargs):
    """Test prog against test cases in database

    :param prog: program file
    :param code: problem code
    :param database: database folder
    :param no_color: do not colorize output
    :param no_custom: do not test against custom added tests
    :param cor_suffix: correct file suffix
    :param inp_suffix: input file suffix
    :param diff_prog: diff program to use
    :param diff_flags: diff flags to use
    :param quiet: supress output

    :type prog: str
    :type code: str
    :type database: str
    :type no_color: Boolean
    :type no_custom: Boolean
    :type cor_suffix: str
    :type inp_suffix: str
    :type diff_prog: str
    :type diff_flags: str
    :type quiet: Boolean

    :return: number of failed tests
    :rtype: int
    """

    def print_color(text, colors=None):
        """Print text in color or not

        :param text: text to print
        :param colors: colors to apply

        :type text: str
        :type colors: list or str
        """
        if not quiet:
            if colors is None or no_color:
                print(text)
                return
            elif not isinstance(colors, list):
                colors = [colors]
            for color in colors:
                print(__ANSI_COLORS__[color], end='')
            print(text)
            for color in colors:
                print(__ANSI_COLORS__['ENDC'], end='')

    if isinstance(prog, str):
        source_file = prog
    else:
        source_file = prog.name

    if source_file.endswith('.cpp') or source_file.endswith('.cc'):

        prog_name = '.'.join(source_file.split('.')[:-1]) + '.x'
        LOG.debug('Compiling to %s', prog_name)

        process = Popen(
            ['g++', '-std=c++11', '-g', source_file, '-o', prog_name])
        return_code = process.wait()

        if return_code:
            LOG.error('Compilation returned %d', return_code)
            exit(return_code)

    else:
        prog_name = source_file

    if prog_name[0] not in ('.', '/'):
        prog_name = './' + prog_name

    cont, cor = 0, 0

    for sample_inp in sorted(
            glob('{}/{}/*.{}'.format(database,
                                     code, inp_suffix))):
        sample_cor = ''.join(sample_inp.split('.')[:-1]) \
                + '.' + cor_suffix

        try:
            test_input = open(sample_inp, 'r')
            test_output = NamedTemporaryFile()

            header_text = '*** Input ' + str(cont) + ' '

            if basename(sample_inp).startswith('custom'):
                if no_custom:
                    continue
                header_text += '(custom) '

            cont += 1

            process = Popen(prog_name, stdin=test_input, stdout=test_output,
                            stderr=PIPE)
            return_code = process.wait()

            if return_code:
                LOG.warning('Program exited with code: %d', return_code)

            test_input.seek(0)

            print_color('{:*<79}'.format(header_text), ['BLUE', 'BOLD'])
            print_color(test_input.read(), 'HEADER')
        finally:
            test_input.close()

        try:
            out = check_output([diff_prog]
                               + diff_flags.split(',')
                               + [test_output.name, sample_cor])
            print_color('{:*<79}'.format('*** OK '), ['GREEN', 'BOLD'])
            print_color(out.decode('UTF-8'))

            cor += 1

        except CalledProcessError as err:   # Thrown if files doesn't match
            print_color('{:*<79}'.format('*** WA '), ['BOLD', 'FAIL'])
            print_color(err.output.decode('UTF-8'))
        finally:
            test_output.close()

    result = ' ({:02}/{:02})'.format(cor, cont)
    if cont == 0:
        print_color('Program has no test-cases yet')
    elif cont == cor:
        print_color('{:*^79}'.format(result + ' ALL OK :) '),
                    ['GREEN', 'BOLD'])
    else:
        print_color('{:*^79}'.format(result + ' :( '), ['FAIL', 'BOLD'])

    return cont-cor
