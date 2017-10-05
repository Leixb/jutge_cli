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
log = logging.getLogger('jutge.download')

from os.path import isdir,isfile,expanduser
from os import mkdir
from tempfile import NamedTemporaryFile

import requests

from . import get_code

class download:
    def __init__(self,args):
        if args.no_download:
            log.error('Remove --no-download flag to download')
            exit(3)

        code = get_code.get_code(args).code
        log.debug(code)
        web = 'https://jutge.org/problems/{}'.format(code)

        from . import cookie

        cookie_container = cookie.cookie(args)

        if cookie_container.has_cookie: cookies = dict(PHPSESSID=cookie_container.cookie)
        else: cookies = {}

        log.debug(cookies)

        if code[0] == 'X':
            if cookies == {}:
                log.error('Cookie needed to download problem')
                exit(25)
            elif cookie_container.check_cookie() == None:
                log.error('Invalid cookie')
                exit(26)

        try: overwrite = args.overwrite
        except AttributeError: overwrite = False

        # Check if already in DB
        db_folder = expanduser('{}/{}'.format(args.database,code))
        if isdir(db_folder) and not overwrite:
            if isfile('{}/problem.html'.format(db_folder,code)):
                log.info('File already in DB, continue')
                return
        else:
            from zipfile import ZipFile

            zip_url = '{}/zip'.format(web)
            log.debug(zip_url)

            response = requests.get(zip_url, cookies=cookies, stream=True)
            temp_zip = NamedTemporaryFile('r+b',suffix='.zip',delete=False)

            for chunk in response.iter_content(chunk_size=1024):
                if chunk: temp_zip.write(chunk)

            temp_zip.close()

            try: zip_file = ZipFile(temp_zip.name, 'r')
            except zipfile.BadZipFile:
                log.error('Could not download zip file')
                exit(23)

            if not isdir(db_folder): mkdir(db_folder)

            zip_file.extractall(db_folder + '/..')
            zip_file.close()

        response = requests.get(web,cookies=cookies)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text,'lxml')

        name = '-'.join(soup.find('title').text.split('-')[1:])
        name = name[1:].replace(' ','_').split()[0]
        if name == 'Error':
            log.error("Couldn't download page, aborting...")
            exit (25)

        # Delete token uid from database
        if cookie_container.check_cookie() != None: 
            soup.find('input', {'name' : 'token_uid'})['value'] = ''

        open('{}/problem.html'.format(db_folder,code),'w').write(str(soup))

