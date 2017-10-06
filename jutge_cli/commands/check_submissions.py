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
log = logging.getLogger('jutge.check_submissions')

import requests
from bs4 import BeautifulSoup

from . import cookie
from . import get_code

class check_submissions:
    def __init__(self,args):

        if args.no_download:
            log.error('Cannot check if --no-download provided')
            exit(20)

        cookie_container = cookie.cookie(args)

        if cookie_container.check_cookie() == None:
            log.error('Invalid cookie')
            exit(25)

        self.cookies = { 'PHPSESSID' : cookie_container.cookie }

        log.debug(args.SUBCOMMAND)

        if args.SUBCOMMAND == 'check_submissions' or args.SUBCOMMAND == 'check': 
            if args.code == None:
                self.check_last(args)
            else:
                code = get_code.get_code(args).code
                veredict = self.check_problem(code)

                if not args.quiet: print(veredict)

                if veredict == 'accepted': exit(0)
                else: exit(1)

    def check_problem(self, code):
        url = 'https://jutge.org/problems/{}'.format(code)

        response = requests.get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text,'lxml')

        open('shit.txt','w').write(response.text)

        for div in soup.findAll('div', {'class' : 'panel-heading'}):
            contents = div.contents[0].strip()
            log.debug(contents)
            if contents.startswith('Problem'):
                return contents.split(':')[1].strip()

    def check_last(self,args):
        url = 'https://jutge.org/submissions'

        response = requests.get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text,'lxml')

        submissions_list = soup.find('ul', {'class' : 'timeline'})

        if args.last:
            submissions_list = [submissions_list.li]
        elif args.reverse:
            submissions_list = submissions_list.findAll('li')[:-1]
            first_veredict = None
        else :
            submissions_list = submissions_list.findAll('li')[-2::-1]

        for submission in submissions_list:
            table = submission.div.table.tr.findAll('td')

            time = table[0].small.contents[0].strip()
            veredict = table[1].small.a.contents[0].strip()

            if args.reverse and first_veredict == None:
                first_veredict = veredict

            problem_code = submission.a['href'].split('/')[2].strip()
            problem_name = submission.div.p.contents[0].strip()

            if not args.quiet: print(time, '\t', veredict, problem_code, problem_name)

        if not args.reverse: first_veredict = veredict

        if first_veredict == 'AC': exit(0)
        else : exit(1)

