#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.archive')

from os.path import isdir,expanduser,isfile,basename
from shutil import move

import show

class archive:
    def __init__(self,args):
        title = show.show(args).title
        ext = basename(args.prog.name).split('.')[-1]
        dest = '{}/{}.{}'.format(expanduser(args.folder),title,ext)

        if not isfile(dest) or args.overwrite: move(args.prog.name,dest)

