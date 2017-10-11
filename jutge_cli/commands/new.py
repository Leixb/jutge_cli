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

from .show import get_title
from .get_code import __expand_subcode__

LOG = getLogger('jutge.new')

TEMPLATES = {
    'cpp' : '''\
#include <bits/stdc++.h>
using namespace std;

int main () {
}
''',
    'py' : '''\
#!/usr/bin/env python3
'''
    }

def new(problem_set, code, **kwargs):
    if problem_set:
        __new_problem_set__(set_name=code, **kwargs)
    else:
        __new_standalone_file__(code=code, **kwargs)

def __new_standalone_file__(code, title, extension, problem_sets,
                            overwrite=False, quiet=False, **kwargs):
    """

    subfolders

    :param code:
    :param title:
    :param extension:
    :param overwrite:
    """
    sub_code = code.split('_')[0]

    dest_folder = '.'

    for sub_folder, problems in problem_sets.items():
        if sub_code in problems:
            dest_folder = sub_folder
            if not isdir(dest_folder):
                mkdir(dest_folder)
            break

    file_name = '{}/{}.{}'.format(dest_folder, title, extension)
    if not isfile(file_name) or overwrite:
        if not quiet:
            print(file_name)
        with open(file_name, 'a') as new_file:
            if extension in TEMPLATES:
                new_file.write(TEMPLATES[extension])

def __new_problem_set__(set_name, problem_sets, extension,
                        overwrite=False, **kwargs):
    """
    :param problem_sets: dict containing all problem sets
    :param set_name: problem set name
    :param extension: extension to use
    :param overwrite: if True overwrite existing files
    """
    try:
        problems = problem_sets[set_name]
    except KeyError:
        LOG.error('Problem set not found')
        return

    if not isdir(set_name):
        mkdir(set_name)

    for subcode in problems:
        code = __expand_subcode__(subcode=subcode, **kwargs)

        if code is None:
            LOG.warning('Could not expand subcode %s, skipping...', subcode)
            continue

        LOG.debug(code)

        title = get_title(code=code, **kwargs)
        file_name = '{}/{}.{}'.format(set_name, title, extension)

        if not isfile(file_name) or overwrite:
            with open(file_name, 'a') as new_file:
                if extension in TEMPLATES:
                    new_file.write(TEMPLATES[extension])
