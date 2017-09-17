#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jgetcode')

import re
from os.path import basename

class jgetcode:
    def __init__(self,args):
        if args.code != '':
            self.code = args.code
            return
        try:
            self.code = re.search("({})".format(args.regex),basename(args.prog)).group(1)
        except AttributeError:
            log.error("Code not found, regex failed")
            exit(26)
