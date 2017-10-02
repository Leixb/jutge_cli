#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.update')

from glob import glob
from os.path import basename,isdir,expanduser
from os import mkdir, symlink
from shutil import copyfile
from tempfile import TemporaryDirectory

from time import sleep

def getname(code,cookie):
    web = 'https://jutge.org/problems/{}'.format(code)

    if cookie != None: cookies = dict(PHPSESSID=cookie)
    else: cookies = {}

    import requests

    response = requests.get(web,cookies=cookies)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.text,'lxml')

    name = '-'.join(soup.find('title').text.split('-')[1:])
    name = name[1:].replace(' ','_').split()[0]

    return name

class update:
    def __init__(self,args):
        from zipfile import ZipFile

        extract_to = TemporaryDirectory().name

        zip = ZipFile(args.zip.name, 'r')
        zip.extractall(extract_to)
        zip.close()

        if not isdir(expanduser(args.folder)): mkdir(expanduser(args.folder))

        extensions = ['cc','c','hs','php','bf','py']

        count = 0

        for folder in glob(extract_to + '/*') :
            # try:
                code = basename(folder)

                sources = []

                for ext in extensions :
                    match = glob('{}/*AC.{}'.format(folder,ext))
                    if match:
                        sources.append([match[-1],ext]) # take last AC

                for source in sources :
                    ext = source[1]
                    if ext == 'cc': ext = 'cpp' # Use cpp over cc for c++ files

                    if not glob('{}/{}*.{}'.format(expanduser(args.folder),code,ext)) or args.overwrite:
                        if args.no_download:
                            name = code
                        else:
                            from . import cookie
                            name = getname(code,cookie.cookie().cookie)

                            if name == 'Error': name = code # If name cannot be found default to code to avoid collisions
                        
                        dest_folder = expanduser(args.folder)

                        file_name = '{}/{}.{}'.format(dest_folder,name,ext)

                        log.info('Copying {} to {} ...'.format(source[0],file_name))
                        copyfile(source[0],file_name)

                        sub_code = code.split('_')[0]
                        sym_link = '.'

                        for sub_folder, problems in defaults.config().subfolders.items():
                            if sub_code in problems:
                                sym_link = '{}/{}'.format(dest_folder,sub_folder)
                                if not isdir(sym_link): mkdir(sym_link)

                        if sym_link != '.':
                            sym_link = '{}/{}.{}'.format(sym_link,name,ext)
                            try:
                                symlink(source, sym_link)
                                log.debug('Symlink {} -> {}'.format(sym_link,source[0]))
                            except FileExistsError:
                                log.warning('Symlink already exists')

                        count += 1

                        if args.delay > 0:
                            sleep(args.delay / 1000.0)

            # except: log.warning('Skipping {}'.format(folder))

        log.info('FINISHED; Added {} programs'.format(count))

