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

from os import mkdir
from os.path import isdir, isfile, expanduser
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, BadZipFile

from bs4 import BeautifulSoup
from requests import get

LOG = getLogger('jutge.download')


def download(code, cookies, database,
             no_download, overwrite=False, **kwargs):
    """
    :param code:
    :param cookies:
    :param database:
    :param no_download:
    :param overwrite:
    """

    if no_download:
        LOG.error('Remove --no-download flag to download')
        exit(3)

    LOG.debug(code)
    web = 'https://jutge.org/problems/{}'.format(code)

    LOG.debug(cookies)

    if code[0] == 'X':
        if cookies == {}:
            LOG.error('Cookie needed to download problem')
            exit(25)

    # Check if already in DB
    db_folder = expanduser('{}/{}'.format(database, code))
    if isdir(db_folder) and not overwrite:
        if isfile('{}/{}/problem.html'.format(db_folder, code)):
            LOG.info('File already in DB, continue')
            return
    else:

        zip_url = '{}/zip'.format(web)
        LOG.debug(zip_url)

        response = get(zip_url, cookies=cookies, stream=True)
        temp_zip = NamedTemporaryFile('r+b', suffix='.zip', delete=False)

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                temp_zip.write(chunk)

        temp_zip.close()

        try:
            zip_file = ZipFile(temp_zip.name, 'r')
        except BadZipFile:
            LOG.error('Could not download zip file')
            exit(23)

        if not isdir(db_folder):
            mkdir(db_folder)

        zip_file.extractall(db_folder + '/..')
        zip_file.close()

    response = get(web, cookies=cookies)

    soup = BeautifulSoup(response.text, 'lxml')

    name = '-'.join(soup.find('title').text.split('-')[1:])
    name = name[1:].replace(' ', '_').split()[0]
    if name == 'Error':
        LOG.error("Couldn't download page, aborting...")
        exit(25)

    # Delete token uid from database
    if cookies != {}:
        soup.find('input', {'name' : 'token_uid'})['value'] = ''

    with open('{}/problem.html'.format(db_folder), 'w') as \
            problem_file:
        problem_file.write(str(soup))
