#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jnew')

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

        new_file = open('{}.{}'.format(title,args.type),'a')

        if (template[args.type] != None ): new_file.write(template[args.type])
