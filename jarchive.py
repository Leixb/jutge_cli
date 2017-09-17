#!/usr/bin/python3

import logging

log = logging.getLogger('jutge.jarchive')

from os.path import isdir,expanduser,isfile
from shutil import move

class jarchive:
    def __init__(self,args):
        title = jprint.jprint(args).title
        dest = '{}/{}'.format(expanduser(args.folder),title)

        if not isfile(dest) or args.overwrite: move(args.prog,dest)

