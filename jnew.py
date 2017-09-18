#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jnew')

from os.path import isfile

import jgetcode
import jprint

template = {
    'cpp':
"""#include <bits/stdc++.h>
using namespace std;

int main () {
}""",
    'py':
"""#!/usr/bin/python3
"""
        }

class jnew:
    def __init__(self,args):
        code = jgetcode.jgetcode(args).code
        title = jprint.jprint(args).title
        file_name = '{}.{}'.format(title,args.type)
        if not isfile(file_name) or args.overwrite: new_file = open(file_name,'a')

        if (template[args.type] != None ): new_file.write(template[args.type])
