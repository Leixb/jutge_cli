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

"""Print title, test-cases or statement of a given problem
"""

from logging import getLogger
from os.path import basename
from glob import glob

from bs4 import BeautifulSoup
try:
    from pypandoc import convert_text
except ModuleNotFoundError:
    PANDOC_LOADED = False
else:
    PANDOC_LOADED = True

from . import download

LOG = getLogger('jutge.show')


def show(code, mode, database, inp_suffix='inp', cor_suffix='cor', **kwargs):
    """
    :param code: problem code
    :param database: database folder
    :param mode: action to perform, one of : ('title', 'stat', 'cases') if None
        return title
    :param inp_suffix: input file suffix for test cases
    :param cor_suffix: output file suffix for test cases
    """

    # Download problem.html if necessary
    download.download(code=code, database=database, **kwargs)

    with open('{}/{}/problem.html'.format(database, code), 'r') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    title = '-'.join(soup.find('title').text.split('-')[1:])
    title = title[1:].replace(' ', '_').split()[0]

    # if mode is None, return title (useful for calls from other modules)
    if mode is None:
        return title

    if mode == 'title':
        print(title)
    elif mode == 'stat':
        # First paragraph removed cause it contains junk
        txt = soup.find('div', id='txt').find_all('p')[1:]

        # Merge into a plain html string
        txt = ' '.join([str(i) for i in txt])

        # Convert html to plain text using pandoc (if loaded)
        if PANDOC_LOADED:
            txt = convert_text(txt, 'plain', 'html')

        print(title + '\n')
        print(txt)

    elif mode == 'cases':
        cont = 0
        for sample_inp in sorted(
                glob('{}/{}/*.{}'.format(database, code, inp_suffix))):
            sample_cor = ''.join(sample_inp.split('.')[:-1])\
                    + '.' + cor_suffix

            if basename(sample_inp).startswith('custom'):
                is_custom = '(custom)'
            else:
                is_custom = ''

            cont += 1

            with open(sample_inp, 'r') as inp_file:
                print('### Input {} {}'.format(cont, is_custom))
                print(inp_file.read())
            with open(sample_cor, 'r') as cor_file:
                print('### Output ' + cont)
                print(cor_file.read())
