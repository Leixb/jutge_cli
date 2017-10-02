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
log = logging.getLogger('jutge.cookie')

from tempfile import gettempdir
from os.path import isfile
from os import remove

class cookie:
    def __init__(self,args):
        self.file_name = '{}/jutge_cli_cookie'.format(gettempdir())
        self.has_cookie = False

        if args.cookie == 'delete': 
            remove(self.file_name)
            return

        try:
            if not (args.cookie is None) and args.cookie != 'print':
                self.cookie = args.cookie
                self.has_cookie = True
                self.make_file()
                return
        except AttributeError: pass
        if isfile(self.file_name):
            file = open(self.file_name)
            self.cookie = file.readline().strip()
            self.has_cookie = True
            file.close()
            log.debug(self.cookie)
        if args.cookie == 'print':
            if self.has_cookie: print(self.cookie)
            else: print('No saved cookie')

    def make_file(self):
        file = open(self.file_name,'w')
        file.write(self.cookie + '\n')
        file.close()
