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

LOG = getLogger('jutge.get_code')


def expand_subcode(subcode, database, no_download, **kwargs):
    """Return code from subcode

    Returns subcode with locale appended (_ca,_en,_es ...)
    None on failure

    :param subcode: subcode
    :param database: database folder path
    :param no_download: do not connect to jutge.org

    :return: code
    :rtype: str
    """

    database = expanduser(database)
    problem_folder = glob('{}/{}_*'.format(database, subcode))

    if problem_folder:
        code = problem_folder[0].split('/')[-1]
    else:

        if no_download:
            LOG.error('Invalid code')
            return None

        url = 'https://jutge.org/problems/' + subcode

        cookie_container = cookie.cookie(no_download=no_download, **kwargs)

        if cookie_container.has_cookie:
            cookies = dict(PHPSESSID=cookie_container.cookie)
        else:
            cookies = {}

        try:
            response = get(url, cookies=cookies)
            soup = BeautifulSoup(response.text, 'lxml')
            code = soup.find('title').text.split('-')[1].strip()
        except KeyError:
            LOG.error('Invalid code')
            return None

        if code == 'Error':
            LOG.error('Invalid code')
            return None
        return code


def get_code(database, regex, no_download, code, prog, **kwargs):
    """Return problem code

    :param database: database folder path
    :param regex: regex used to match code
    :param no_download: do not connect to jutge.org

    :param code: problem code
    :param prog: problem file
    """

    try:
        if code is not None:

            if '_' not in code:
                code = expand_subcode(
                    code, database=database,
                    no_download=no_download, **kwargs)

            LOG.debug('code in args')
            LOG.debug(code)

            return code
    except AttributeError:
        pass

    if isinstance(prog, str):
        prog_name = basename(prog)
    else:
        prog_name = basename(prog.name)

    try:
        code = search('({})'.format(regex), prog_name).group(1)
        LOG.debug(code)
    except AttributeError:
        LOG.warning('Code not found falling back to normal regex')
        try:
            regex_v2 = regex.split('_')[0]
            subcode = search('({})'.format(regex_v2), prog_name).group(1) + '_ca'
            code = expand_subcode(
                subcode, database=database,
                no_download=no_download, **kwargs)

            if code is None:
                return subcode
            return code

        except AttributeError:
            LOG.error('Code not found, regex failed')
            return None
