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
from os import mkdir
from os.path import isfile, isdir

from . import defaults
from . import get_code
from . import show

log = getLogger('jutge.new')

template = {
    'cpp': '''\
#include <bits/stdc++.h>
using namespace std;

int main () {
}
''',
    'py': '''\
#!/usr/bin/python3
'''
        }


class new:

    def __init__(self, args):
        if args.problem_set:
            self.problem_set(args)
        else:
            self.standalone_file(args)

    def standalone_file(self, args):
        code = get_code.get_code(args).code
        sub_code = code.split('_')[0]
        title = show.show(args).title

        dest_folder = '.'

        for sub_folder, problems in defaults.config().subfolders.items():
            if sub_code in problems:
                dest_folder = sub_folder
                if not isdir(dest_folder):
                    mkdir(dest_folder)
                break

        file_name = '{}/{}.{}'.format(dest_folder, title, args.type)
        if not isfile(file_name) or args.overwrite:
            with open(file_name, 'a') as new_file:
                if template[args.type] is not None:
                    new_file.write(template[args.type])

    def problem_set(self, args):
        try:
            problems = defaults.config().subfolders[args.code]
        except KeyError:
            log.error('Problem set not found')
            exit(20)

        dest_folder = args.code
        if not isdir(dest_folder):
            mkdir(dest_folder)

        args_dict = vars(args)

        for subcode in problems:
            args_dict['code'] = subcode
            code = get_code.get_code(args).code

            log.debug(code)

            title = show.show(args).title
            file_name = '{}/{}.{}'.format(dest_folder, title, args.type)

            if not isfile(file_name) or args.overwrite:
                with open(file_name, 'a') as new_file:
                    if template[args.type] is not None:
                        new_file.write(template[args.type])
