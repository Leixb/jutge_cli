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
log = logging.getLogger('jutge.new')

from os.path import isfile,isdir
from os import mkdir

from . import get_code
from . import show
from . import defaults

template = {
    'cpp':
'''#include <bits/stdc++.h>
using namespace std;

int main () {
}''',
    'py':
'''#!/usr/bin/python3
'''
        }

class new:
    def __init__(self,args):
        code = get_code.get_code(args).code
        sub_code = code.split('_')[0]
        title = show.show(args).title

        dest_folder = '.'

        for sub_folder, problems in defaults.config().subfolders.items():
            if sub_code in problems:
                dest_folder = sub_folder
                if not isdir(dest_folder): mkdir(dest_folder)
                break

        file_name = '{}/{}.{}'.format(dest_folder,title,args.type)
        if not isfile(file_name) or args.overwrite: new_file = open(file_name,'a')


        if (template[args.type] != None ): new_file.write(template[args.type])

