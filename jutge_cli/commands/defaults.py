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
log = logging.getLogger('jutge.defaults')

import yaml
from os.path import expanduser

class config:
    def __init__(self):

        try:
            with open(expanduser('~/.jutge_cli.yaml'),'r') as config_file:
                settings = yaml.load(config_file)
        except FileNotFoundError:
            log.warning('No config file round')
            settings = {}

        self.param = dict(
            database = '~/Documents/jutge/DB',
            regex = '[PGQX]\d{5}_(ca|en|es)',
            diff-prog = 'diff',
            diff-flags = '-y',
            inp-suffix = 'inp',
            cor-suffix = 'cor',
            folder = '~/Documents/jutge/Done',
        )

        self.subfolders = {}

        try: self.param['regex'] = settings['regex']
        except KeyError: pass
        try: self.param['database'] = settings['database']
        except KeyError: pass
        try: self.param['diff-prog'] = settings['diff-prog']
        except KeyError: pass
        try: self.param['diff-flags'] = settings['diff-flags']
        except KeyError: pass
        try: self.param['inp-suffix'] = settings['inp-suffix']
        except KeyError: pass
        try: self.param['cor-suffix'] = settings['cor-suffix']
        except KeyError: pass
        try: self.param['folder'] = settings['folder']
        except KeyError: pass
        try: self.subfolders = settings['problem_sets']
        except KeyError: pass

