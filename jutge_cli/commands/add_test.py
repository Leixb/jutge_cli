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

"""This method provides the function `add_test` that creates the necesary files
to add a new test case to the database folder
"""

from glob import glob
from logging import getLogger
from os import mkdir, remove
from os.path import isdir, expanduser, basename
from re import search
from sys import stdin

LOG = getLogger('jutge.add_test')


def add_test(database, code, delete, input_file, output_file, 
        inp_suffix, cor_suffix, **kwargs):
    """Add custom test to database

    :param database: database folder
    :param code: problem code
    :param delete: delete tests
    :param input_file: file containing test case input
    :param output_file: file containing test case output
    :param inp_suffix: input file suffix
    :param cor_suffix: output file suffix

    :type database: str
    :type code: str
    :type delete: Boolean
    :type input_file: FileType('r')
    :type output_file: FileType('r')
    :type inp_suffix: str
    :type cor_suffix: str
    """

    dest_folder = expanduser('{}/{}'.format(database, code))

    if delete:
        for custom_test in glob('{}/custom-*'.format(dest_folder)):
            remove(custom_test)
        return

    if input_file == stdin:
        print('Enter input:')
    src_inp = input_file.read()
    if output_file == stdin:
        print('Enter output:')
    src_cor = output_file.read()

    if not isdir(dest_folder):
        mkdir(dest_folder)

    files = sorted(glob('{}/custom-*'.format(dest_folder)))
    if files:
        num = 1 + int(search('-([0-9]*).', basename(files[-1])).group(1))
    else:
        num = 0

    dest = '{folder}/custom-{n:02}'.format(folder=dest_folder, n=num)

    with open('{}.{}'.format(dest, inp_suffix), 'w') as inp_file:
        inp_file.write(src_inp)
    with open('{}.{}'.format(dest, cor_suffix), 'w') as cor_file:
        cor_file.write(src_cor)
