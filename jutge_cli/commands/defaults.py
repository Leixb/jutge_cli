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
from os.path import expanduser

from yaml import load

log = getLogger('jutge.defaults')

class config:

    def __init__(self):

        try:
            with open(expanduser('~/.jutge_cli.yaml'), 'r') as config_file:
                settings = load(config_file)
        except FileNotFoundError:
            log.warning('No config file round')
            settings = {}

        self.param = {
            'database' : '~/Documents/jutge/DB',
            'regex' : '[PGQX]\d{5}_(ca|en|es)',
            'diff-prog' : 'diff',
            'diff-flags' : '-y',
            'inp-suffix' : 'inp',
            'cor-suffix' : 'cor',
            'folder' : '~/Documents/jutge/Done',
            'email' : None,
            'password' : None
        }

        self.subfolders = {}

    for key in self.param.iterkeys() + ['problem_sets']:
        try:
            if key in ('email', 'password'):
                self.param[key] = settings['login'][key]
            elif key == 'problem_sets':
                self.subfolders = settings[key]
            else:
                self.param[key] = settings[key]
        except KeyError:
            pass

