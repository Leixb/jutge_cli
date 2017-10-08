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
from os import mkdir, remove
from os.path import isdir, expanduser, basename
from re import search
from sys import stdin

from . import get_code

log = getLogger('jutge.add_test')

class add_test:

    def __init__(self, args):

        code = get_code.get_code(args).code
        dest_folder = expanduser('{db}/{code}'.format(args.database, code))

        if args.delete:
            for custom_test in glob('{}/custom-*'.format(dest_folder)):
                remove(custom_test)
            return

        if args.input_file == stdin:
            print('Enter input:')
        src_inp = args.input_file.read()
        if args.output_file == stdin:
            print('Enter output:')
        src_cor = args.output_file.read()

        if not isdir(dest_folder):
            mkdir(dest_folder)

        files = sorted(glob('{}/custom-*'.format(dest_folder)))
        if files:
            n = 1 + int(search('-([0-9]*).', basename(files[-1])).group(1))
        else:
            n = 0

        dest = '{folder}/custom-{n}'.format(folder=dest_folder, n=n)

        with open('{}.{}'.format(dest, args.inp_suffix), 'a') as inp_file:
            inp_file.write(src_inp)
        with open('{}.{}'.format(dest, args.cor_suffix), 'a') as cor_file:
            cor_file.write(src_cor)

