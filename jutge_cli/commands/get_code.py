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


from glob import glob
from logging import getLogger
from os.path import basename, expanduser
from re import search

from bs4 import BeautifulSoup
from requests import get

from . import cookie

log = getLogger('jutge.get_code')

class get_code:

    def __init__(self, args):
        try:
            if args.code != None:
                self.code = args.code

                if not '_' in self.code:
                    db_folder = glob(expanduser('{}/{}_*'.format(args.database,
                        self.code)))

                    if len(db_folder)!=0:
                        self.code = db_folder[0].split('/')[-1]
                    else:

                        if args.no_download:
                            log.error('Invalid code')
                            exit(3)


                        url = 'https://jutge.org/problems/' + args.code

                        cookie_container = cookie.cookie(args)

                        if cookie_container.has_cookie:
                            cookies = dict(PHPSESSID=cookie_container.cookie)
                        else:
                            cookies = {}

                        try:
                            self.code = BeautifulSoup(
                                    get(url, cookies=cookies).text, 'lxml'
                                ).find('title').text.split('-')[1].strip()
                        except KeyError:
                            log.error('Invalid code')
                            exit(4)

                        if self.code == 'Error':
                            log.error('Invalid code')
                            exit(3)

                log.debug('code in args')
                log.debug(self.code)
                return
        except AttributeError: pass

        if isinstance(args.prog, str):
            prog_name = args.prog
        else:
            prog_name = args.prog.name

        try:
            self.code = search('({})'.format(args.regex),
                    basename(prog_name)).group(1)
            log.debug(self.code)
        except AttributeError:
            log.warning('Code not found falling back to normal regex')
            try:
                self.code = search('({})'.format(args.regex.split('_')[0]),
                        basename(prog_name)).group(1) + '_ca'
                return
            except AttributeError:
                log.error('Code not found, regex failed')
                exit(26)

