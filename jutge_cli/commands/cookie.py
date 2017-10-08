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
from os import remove
from os.path import isfile
from tempfile import gettempdir

from bs4 import BeautifulSoup
from requests import get

log = getLogger('jutge.cookie')

class cookie:

    def __init__(self, args):
        self.file_name = '{}/jutge_cli_cookie'.format(gettempdir())
        self.has_cookie = False
        self.check_done = False

        self.no_download = args.no_download

        if args.cookie == 'delete':
            remove(self.file_name)
            return

        try:
            if not args.cookie in (None, 'show', 'print'):
                self.cookie = args.cookie
                self.has_cookie = True
                if not args.skip_check:
                    if self.check_cookie() == None:
                        log.error('Invalid cookie (if you want to \
                                skip the check use --skip-check)')
                        exit(3)
                self.make_file()
                return
        except AttributeError: pass
        if isfile(self.file_name):
            with open(self.file_name) as cookie_file:
                self.cookie = cookie_file.readline().strip()
                self.has_cookie = True
            log.debug(self.cookie)

        if args.cookie == 'print' or args.cookie == 'show':
            if self.has_cookie:
                print(self.cookie)
            else:
                log.warning('No cookie saved')

    def make_file(self):
        with open(self.file_name, 'w') as cookie_file:
            cookie_file.write(self.cookie + '\n')

    def check_cookie(self):
        if self.check_done:
            return self.username

        if self.no_download:
            log.debug('Cannot check cookie if no-download active')
            return None

        cookies = { 'PHPSESSID' : self.cookie }
        web = 'https://jutge.org/dashboard'

        response = get(web, cookies=cookies)
        soup = BeautifulSoup(response.text, 'lxml')

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

        except AttributeError:
            log.debug('Invalid cookie: {}'.format(self.cookie))
            self.username = None

        self.check_done = True
        return self.username

