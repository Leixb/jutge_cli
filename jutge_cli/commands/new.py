#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.new')

from os.path import isfile,isdir
from os import mkdir

from . import get_code
from . import show
from . import defaults

template = {
    'cpp':
'''#include <bits/stdc++.h>
using namespace std;

int main () {
}''',
    'py':
'''#!/usr/bin/python3
'''
        }

class new:
    def __init__(self,args):
        code = get_code.get_code(args).code
        sub_code = code.split('_')[0]
        title = show.show(args).title

        dest_folder = '.'

        for sub_folder, problems in defaults.config().subfolders.items():
            if sub_code in problems:
                dest_folder = sub_folder
                if not isdir(dest_folder): mkdir(dest_folder)
                break

        file_name = '{}/{}.{}'.format(dest_folder,title,args.type)
        if not isfile(file_name) or args.overwrite: new_file = open(file_name,'a')


        if (template[args.type] != None ): new_file.write(template[args.type])

