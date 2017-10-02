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


import logging
log = logging.getLogger('jutge.show')

from os.path import expanduser, basename
from glob import glob

from . import get_code
from . import download

from bs4 import BeautifulSoup

class show:
    def __init__(self,args):
        code = get_code.get_code(args).code

        download.download(args) # Download problem.html if necessary

        html = open('{}/{}/problem.html'.format(expanduser(args.database),code),'r')
        soup = BeautifulSoup(html,'lxml')
        self.title = '-'.join(soup.find('title').text.split('-')[1:])
        self.title = self.title[1:].replace(' ','_').split()[0]

        try:
            if args.mode == 'title': print(self.title)
            elif args.mode == 'stat':
                import pypandoc
                # Find statements in html. First paragraph removed cause it contains junk
                txt = soup.find('div',id='txt').find_all('p')[1:] 

                # Merge into a plain html string
                txt = ' '.join([str(i) for i in txt])

                # Convert html to plain text using pandoc
                txt = pypandoc.convert_text(txt,'plain','html')
                print(self.title + '\n')
                print(txt)

            elif args.mode == 'cases':
                cont = 0
                for sample_inp in sorted(glob('{}/{}/*.{}'.format(expanduser(args.database),code,args.inp_suffix))):
                    sample_cor = ''.join(sample_inp.split('.')[:-1]) + '.' + args.cor_suffix

                    if basename(sample_inp).startswith('custom'): is_custom = '(custom)'
                    else: is_custom = ''

                    cont+=1

                    print('### Input {} {}'.format(cont, is_custom))
                    print(open(sample_inp,'r').read())
                    print('### Output {}'.format(cont))
                    print(open(sample_cor,'r').read())
        except AttributeError:
            pass

