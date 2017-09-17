#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jupdate')

from glob import glob
from os.path import basename,isdir,expanduser
from os import mkdir
from shutil import copyfile
from tempfile import gettempdir

def getname(code):
    web = 'https://jutge.org/problems/{}'.format(code)

    if args.cookie != None: cookies = dict(PHPSESSID=args.cookie)
    else: cookies = {}

    response = requests.get(web,cookies=cookies)

    soup = BeautifulSoup(response.text,'lxml')

    name = "-".join(soup.find('title').text.split('-')[1:])
    name = name[1:].replace(' ','_').split()[0]

    return name

class jupdate:
    def __init__(self,args):
        from zipfile import ZipFile

        extract_to = gettempdir() + '/process_jutge_TMP'

        zip = ZipFile(args.zip.name, 'r')
        mkdir(extract_to)
        zip.extractall(extract_to)
        zip.close()

        if not isdir(expanduser(args.folder)): mkdir(expanduser(args.folder))

        extensions = ['cc','c','hs','php','bf','py']

        count = 0

        for folder in glob(extract_to + '/*') :
            try:
                code = basename(folder)

                sources = []

                for ext in extensions :
                    match = glob('{}/*AC.{}'.format(folder,ext))
                    if match:
                        sources.append([match[-1],ext]) # take last AC

                for source in sources :
                    ext = source[1]
                    if ext == 'cc': ext = 'cpp' # Use cpp over cc for c++ files

                    if not glob('{}/{}*.{}'.format(expanduser(args.folder),code,ext)) or args.overwritte:
                        if args.no_download:
                            name = code
                        else:
                            name = getname(code)

                            if name == 'Error': name = code # If name cannot be found default to code to avoid collisions

                        file_name = '{}/{}.{}'.format(expanduser(args.folder),name,ext)

                        log.info('Copying {} to {} ...'.format(source[0],file_name))
                        copyfile(source[0],file_name)

                        count += 1

                        if args.delay > 0:
                            sleep(args.delay / 1000.0)

            except: log.warning('Skipping {}'.format(folder))

        log.info('FINISHED; Added {} programs'.format(count))
