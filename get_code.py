#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.get_code')

import re
from os.path import basename

class get_code:
    def __init__(self,args):
        if args.code != None:
            self.code = args.code
            log.debug('code in args')
            log.debug(args.code)
            return
        try:
            self.code = re.search("({})".format(args.regex),basename(args.prog.name)).group(1)
            log.debug(self.code)
        except AttributeError:
            log.warning("Code not found falling back to normal regex")
            try:
                self.code = re.search("({})".format(args.regex.split('_')[0]),basename(args.prog.name)).group(1) + '_ca'
                return
            except AttributeError:
                log.error("Code not found, regex failed")
                exit(26)

