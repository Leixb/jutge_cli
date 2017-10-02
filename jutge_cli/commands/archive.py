#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.archive')

from . import get_code

from os import mkdir, symlink, remove
from os.path import isdir,expanduser,isfile,basename
from shutil import move, copyfile

from . import show
from . import defaults

class archive:
    def __init__(self,args):
        title = show.show(args).title
        ext = basename(args.prog.name).split('.')[-1]

        dest_folder = expanduser(args.folder)
        sym_link = '.'

        code = get_code.get_code(args).code
        sub_code = code.split('_')[0]

        for sub_folder, problems in defaults.config().subfolders.items():
            if sub_code in problems:
                sym_link = '{}/{}'.format(dest_folder,sub_folder)
                if not isdir(sym_link): mkdir(sym_link)

        source = '{}/{}.{}'.format(dest_folder,title,ext)
        if not isfile(source) or args.overwrite: 
            if not args.no_delete: move(args.prog.name,source)
            else: copyfile(args.prog.name,source)

        if sym_link != '.':
            sym_link = '{}/{}.{}'.format(sym_link,title,ext)
            try:
                symlink(source, sym_link)
                log.debug('Symlink {} -> {}'.format(sym_link,source))
                if isfile(args.prog.name) and not args.no_delete: remove(args.prog.name)
            except FileExistsError:
                log.error('Symlink already exists')

        log.debug(source)

