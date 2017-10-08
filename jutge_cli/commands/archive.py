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
from os import mkdir, symlink, remove
from os.path import isdir, expanduser, isfile, basename
from shutil import move, copyfile

from . import defaults
from . import get_code
from . import show

log = getLogger('jutge.archive')

class archive:

    def __init__(self, args):
        title = show.show(args).title
        ext = basename(args.prog.name).split('.')[-1]

        dest_folder = expanduser(args.folder)
        sym_link = '.'

        code = get_code.get_code(args).code
        sub_code = code.split('_')[0]

        for sub_folder, problems in defaults.config().subfolders.items():
            if sub_code in problems:
                sym_link = '{}/{}'.format(dest_folder, sub_folder)
                if not isdir(sym_link):
                    mkdir(sym_link)

        source = '{}/{}.{}'.format(dest_folder, title, ext)
        if not isfile(source) or args.overwrite:
            if not args.no_delete:
                move(args.prog.name, source)
            else:
                copyfile(args.prog.name, source)

        if sym_link != '.':
            sym_link = '{}/{}.{}'.format(sym_link, title, ext)
            try:
                symlink(source, sym_link)
                log.debug('Symlink {} -> {}'.format(sym_link, source))
                if isfile(args.prog.name) and not args.no_delete:
                    remove(args.prog.name)
            except FileExistsError:
                log.error('Symlink already exists')

        log.debug(source)

