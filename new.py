#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.new')

from os.path import isfile

import getcode
import show

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

class new:
    def __init__(self,args):
        code = get_code.get_code(args).code
        title = show.show(args).title
        file_name = '{}.{}'.format(title,args.type)
        if not isfile(file_name) or args.overwrite: new_file = open(file_name,'a')

        if (template[args.type] != None ): new_file.write(template[args.type])

