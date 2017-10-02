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
log = logging.getLogger('jutge.upload')

import requests
from bs4 import BeautifulSoup

from . import get_code

class upload:
    def __init__(self,args):

        if args.no_download:
            log.error('Remove --no-download flag to upload')
            exit(4)

        code = get_code.get_code(args).code
        log.debug(code)

        web = 'https://jutge.org/problems/{}/submissions'.format(code)
        log.debug(web)

        from . import cookie

        cookie_container = cookie.cookie(args)

        if cookie_container.has_cookie: cookies = dict(PHPSESSID=cookie_container.cookie)
        else:
            log.error("We need cookie to upload")
            exit(25)

        # We need token_uid for POST to work

        response = requests.get(web, cookies=cookies)
        soup = BeautifulSoup(response.text,'lxml')

        token_uid = soup.find('input', {'name' : 'token_uid'})['value']
        log.debug(token_uid)

        extension = args.prog.name.split('.')[-1] # To determine compiler

        compiler = dict(
                ada = 'GNAT',
                bas = 'FBC',
                bf = 'BEEF',
                c = 'GCC',
                cc = 'P1++',
                cpp = 'G++11',
                cs = 'MonoCS',
                d = 'GDC',
                erl = 'Erlang',
                f = 'GFortran',
                go = 'Go',
                hs = 'GHC',
                java = 'JDK',
                js = 'nodejs',
                lisp = 'CLISP',
                lua = 'Lua',
                m = 'GObjC',
                pas = 'FPC',
                php = 'PHP',
                pl = 'Perl',
                py = 'Python3',
                py2 = 'Python',
                r = 'R',
                rb = 'Ruby',
                scm = 'Chicken',
                v = 'Verilog',
                ws = 'WS',
                )

        if not args.compiler is None: compiler[extension] = args.compiler

        data = {
                'annotation' : 'Uploaded by jutge_cli', 
                'compiler_id' : compiler[extension], 
                'submit' : 'submit',
                'token_uid' : token_uid
                }

        log.debug(data)

        files= {
                'file' : open(args.prog.name,'r')
                }

        requests.post(web, data=data, files=files, cookies=cookies)

