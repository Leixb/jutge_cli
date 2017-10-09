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

"""Provides class Check_submissions that connects to jutge.org and fetches
the checks the last submissions veredict

Check_submissions provides different methods to check the either the veredict
of the last submission or the veredict of the last submission of a specific
problem
"""

from logging import getLogger

from bs4 import BeautifulSoup
from requests import get

from . import cookie
from . import get_code

LOG = getLogger('jutge.check_submissions')


def check_submissions(args):
    """Wrap CheckSubmissions class into function

    :param args: argparse flags
    :type args: argparse.Namespace
    """
    return CheckSubmissions(args)


class CheckSubmissions:

    """Check last submissions to jutge.org
    """

    def __init__(self, args):
        """Save copy of args to the class

        If it is called from jutge.py subcommand it will call method
        check_last() or check_problem() depending if args.code exists

        :param args: argparse flags
        :type args: argparse.Namespace
        """

        if args.no_download:
            LOG.error('Cannot check if --no-download provided')
            exit(20)

        self.args = args

        cookie_container = cookie.cookie(self.args)

        if cookie_container.check_cookie() is None:
            LOG.error('Invalid cookie')
            exit(25)

        self.cookies = {'PHPSESSID' : cookie_container.cookie}

        LOG.debug(self.args.SUBCOMMAND)

        if self.args.SUBCOMMAND in ('check_submissions', 'check'):
            if self.args.code is None:
                if self.check_last()['veredict'] in ('AC', '100/100'):
                    exit(0)
                else:
                    exit(1)
            else:
                code = get_code.get_code(self.args).code
                veredict = self.check_problem(code)

                if not self.args.quiet:
                    print(veredict)

                if veredict == 'accepted':
                    exit(0)
                else:
                    exit(1)

    def check_problem(self, code):
        """Check last submission of a given problem code

        :param code: string equal to the jutge.org code of the problem to check
        :return: problem veredict
        :rtype: str
        """

        url = 'https://jutge.org/problems/{}'.format(code)

        response = get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'lxml')

        for div in soup.findAll('div', {'class' : 'panel-heading'}):
            contents = div.contents[0].strip()
            LOG.debug(contents)
            if contents.startswith('Problem'):
                return contents.split(':')[1].strip()

    def check_last(self):
        """Check last submissions to jutge.org

        This function will connect to jutge.org and retrieve the last
        submissions veredicts and output them. The following argparse
        flags modify it's behaviour:
            args.quiet: no print, only return veredict
            args.last: print only the last submission
            args.reverse: print the first submission last

        :return: last veredict in the form of a dict with keys:
            code, time and veredict
        :rtype: dict
        """

        url = 'https://jutge.org/submissions'

        response = get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'lxml')

        submissions_list = soup.find('ul', {'class' : 'timeline'})

        if self.args.last:
            submissions_list = [submissions_list.li]
        elif self.args.reverse:
            submissions_list = submissions_list.findAll('li')[:-1]
            last_veredict = None
        else:
            submissions_list = submissions_list.findAll('li')[-2::-1]

        for submission in submissions_list:
            table = submission.div.table.tr.findAll('td')

            time = table[0].small.contents[0].strip()
            veredict = table[1].small.a.contents[0].strip()

            problem_code = submission.a['href'].split('/')[2].strip()
            problem_name = submission.div.p.contents[0].strip()

            if self.args.reverse and last_veredict is None:
                last_veredict = dict(
                    veredict=veredict, code=problem_code, time=time)

            if not self.args.quiet:
                print('{:>19} {:^9} {:>8} {}'.format(
                    time, veredict, problem_code, problem_name))

        if not self.args.reverse:
            last_veredict = dict(
                veredict=veredict, code=problem_code, time=time)

        return last_veredict
