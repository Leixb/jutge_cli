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
        self.check_done = False

        self.no_download = args.no_download

        if args.cookie == 'delete': 
            remove(self.file_name)
            return

        try:
            if not (args.cookie is None) and args.cookie != 'print' and args.cookie != 'show':
                self.cookie = args.cookie
                self.has_cookie = True
                if not args.skip_check:
                    if self.check_cookie() == None:
                        log.error('Invalid cookie, if you want to skip the check use --skip-check')
                        exit(3)
                self.make_file()
                return
        except AttributeError: pass
        if isfile(self.file_name):
            file = open(self.file_name)
            self.cookie = file.readline().strip()
            self.has_cookie = True
            file.close()
            log.debug(self.cookie)
        if args.cookie == 'print' or args.cookie == 'show':
            if self.has_cookie: print(self.cookie)
            else: print('No saved cookie')

    def make_file(self):
        file = open(self.file_name,'w')
        file.write(self.cookie + '\n')
        file.close()

    def check_cookie(self):

        if self.check_done: return self.username

        if self.no_download:
            log.debug('Cannot check cookie if no-download active')
            return None

        import requests
        from bs4 import BeautifulSoup

        cookies = { 'PHPSESSID' : self.cookie }
        web = 'https://jutge.org/dashboard'

        response = requests.get(web, cookies=cookies)
        soup = BeautifulSoup(response.text,'lxml')

        try:
            tags = soup.findAll('a', {'href' : '/profile'})
            for tag in tags:
                log.debug(tag.b)
                if tag.b != None:
                    self.username = tag.b.contents[0]
                    log.debug(tag.b)
                    break

            log.debug(self.username)
            log.debug('Logged in as: {}'.format(self.username))

            self.check_done = True
            return self.username
        except AttributeError:
            self.username = None
            log.debug('Invalid cookie: {}'.format(self.cookie))

            self.check_done = True
            return self.username

