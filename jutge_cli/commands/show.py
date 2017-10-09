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

from logging import getLogger
from os.path import expanduser, basename
from glob import glob

from bs4 import BeautifulSoup
try:
    from pypandoc import convert_text
except ModuleNotFoundError:
    pandoc_loaded = False
else:
    pandoc_loaded = True

from . import get_code
from . import download

log = getLogger('jutge.show')

class show:

    def __init__(self, args):
        code = get_code.get_code(args).code

        download.download(args) # Download problem.html if necessary

        with open('{}/{}/problem.html'.format(
                expanduser(args.database), code), 'r') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
        self.title = '-'.join(soup.find('title').text.split('-')[1:])
        self.title = self.title[1:].replace(' ', '_').split()[0]

        try:
            if args.mode == 'title':
                print(self.title)
            elif args.mode == 'stat':
                # First paragraph removed cause it contains junk
                txt = soup.find('div', id='txt').find_all('p')[1:]

                # Merge into a plain html string
                txt = ' '.join([str(i) for i in txt])

                # Convert html to plain text using pandoc (if loaded)
                if pandoc_loaded:
                    txt = convert_text(txt, 'plain', 'html')

                print(self.title + '\n')
                print(txt)

            elif args.mode == 'cases':
                cont = 0
                for sample_inp in sorted(glob(
                        '{}/{}/*.{}'.format(expanduser(args.database),
                        code, args.inp_suffix))):
                    sample_cor = ''.join(sample_inp.split('.')[:-1])\
                            + '.' + args.cor_suffix

                    if basename(sample_inp).startswith('custom'):
                        is_custom = '(custom)'
                    else:
                        is_custom = ''

                    cont+=1

                    with open(sample_inp, 'r') as inp_file:
                        print('### Input {} {}'.format(cont, is_custom))
                        print(inp_file.read())
                    with open(sample_cor, 'r') as cor_file:
                        print('### Output ' + cont)
                        print(cor_file.read())
        except AttributeError:
            pass

