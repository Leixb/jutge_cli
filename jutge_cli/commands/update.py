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
from os import mkdir, symlink
from os.path import basename, isdir, expanduser
from shutil import copyfile
from tempfile import TemporaryDirectory
from time import sleep

from bs4 import BeautifulSoup
from requests import get
from zipfile import ZipFile

from . import cookie

log = getLogger('jutge.update')

def getname(code, cookie):
    web = 'https://jutge.org/problems/{}'.format(code)

    if cookie != None:
        cookies = dict(PHPSESSID=cookie)
    else:
        cookies = {}

    response = get(web, cookies=cookies)

    soup = BeautifulSoup(response.text, 'lxml')

    name = '-'.join(soup.find('title').text.split('-')[1:])
    name = name[1:].replace(' ', '_').split()[0]

    return name

class update:

    def __init__(self, args):

        extract_to = TemporaryDirectory().name

        zip = ZipFile(args.zip.name, 'r')
        zip.extractall(extract_to)
        zip.close()

        if not isdir(expanduser(args.folder)):
            mkdir(expanduser(args.folder))

        extensions = ['cc', 'c', 'hs', 'php', 'bf', 'py']

        count = 0

        for folder in glob(extract_to + '/*') :
            # try:
                code = basename(folder)

                sources = []

                for ext in extensions :
                    match = glob('{}/*AC.{}'.format(folder, ext))
                    if match:
                        sources.append([match[-1], ext]) # take last AC

                for source in sources :
                    ext = source[1]
                    if ext == 'cc': ext = 'cpp' # Use cpp over cc for c++ files

                    if not glob('{}/{}*.{}'.format(expanduser(args.folder), code, ext)) or args.overwrite:
                        if args.no_download:
                            name = code
                        else:
                            name = getname(code, cookie.cookie().cookie)

                            if name == 'Error': name = code # If name cannot be found default to code to avoid collisions

                        dest_folder = expanduser(args.folder)

                        file_name = '{}/{}.{}'.format(dest_folder, name, ext)

                        log.info('Copying {} to {} ...'.format(source[0], file_name))
                        copyfile(source[0], file_name)

                        sub_code = code.split('_')[0]
                        sym_link = '.'

                        for sub_folder, problems in defaults.config().subfolders.items():
                            if sub_code in problems:
                                sym_link = '{}/{}'.format(dest_folder, sub_folder)
                                if not isdir(sym_link): mkdir(sym_link)

                        if sym_link != '.':
                            sym_link = '{}/{}.{}'.format(sym_link, name, ext)
                            try:
                                symlink(source, sym_link)
                                log.debug('Symlink {} -> {}'.format(sym_link, source[0]))
                            except FileExistsError:
                                log.warning('Symlink already exists')

                        count += 1

                        if args.delay > 0:
                            sleep(args.delay / 1000.0)

            # except: log.warning('Skipping {}'.format(folder))

        log.info('FINISHED; Added {} programs'.format(count))

