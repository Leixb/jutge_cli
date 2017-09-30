#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.cookie')

from tempfile import gettempdir
from os.path import isfile
from os import remove

class cookie:
    def __init__(self,args):
        self.file_name = '{}/jutge_cli_cookie'.format(gettempdir())
        self.has_cookie = False

        try: 
            if args.delete: remove(self.file_name)
            return
        except AttributeError: pass

        try:
            if not (args.cookie is None):
                self.cookie = args.cookie
                self.has_cookie = True
                self.make_file()
                return
        except AttributeError: pass
        if isfile(self.file_name):
            file = open(self.file_name)
            self.cookie = file.readline().strip()
            self.has_cookie = True
            file.close()
            log.debug(self.cookie)

    def make_file(self):
        file = open(self.file_name,'w')
        file.write(self.cookie)
        file.write('\n')
        file.close()
