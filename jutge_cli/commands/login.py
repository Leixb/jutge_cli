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
log = logging.getLogger('jutge.login')

from getpass import getpass
import requests

from . import cookie

class login:
    def __init__(self,args):

        url = 'https://jutge.org/'
        login_data = {
            'email': 'aleix.bone@est.fib.upc.edu',
            'password': getpass('Password: '),
            'submit': ''
        }
        s = requests.Session()
        s.post(url, data=login_data)

        session_cookie = requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']

        log.debug(session_cookie)
        
        vars(args)['cookie'] = session_cookie
        vars(args)['skip-check'] = False

        cookie.cookie(args).make_file()

