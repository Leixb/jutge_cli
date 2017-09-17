#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jdownload')

from os.path import isdir,isfile,expanduser
from os import mkdir
from tempfile import NamedTemporaryFile

import requests

import jgetcode

class jdownload:
    def __init__(self,args):
        if args.no_download:
            log.error('Remove --no-download flag to download')
            exit(3)

        code = jgetcode.jgetcode(args).code
        web = 'https://jutge.org/problems/{}'.format(code)

        if args.cookie != '': cookies = dict(PHPSESSID=args.cookie)
        else: cookies = {}

        # Check if already in DB
        db_folder = expanduser('{}/{}'.format(args.database,code))
        if isdir(db_folder) and not args.overwrite:
            if isfile('{}/problem.html'.format(db_folder,code)):
                log.info('File already in DB, continue')
                return
        else:
            mkdir(db_folder)
            from zipfile import ZipFile

            zip_url = "{}/zip".format(web)

            response = requests.get(zip_url, cookies=cookies, stream=True)
            temp_zip = NamedTemporaryFile('r+b',suffix='.zip',delete=False)

            for chunk in response.iter_content(chunk_size=1024):
                if chunk: temp_zip.write(chunk)

            temp_zip.close()

            zip_file = ZipFile(temp_zip.name, 'r')
            zip_file.extractall(db_folder + '/..')
            zip_file.close()

        response = requests.get(web,cookies=cookies)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text,'lxml')

        name = "-".join(soup.find('title').text.split('-')[1:])
        name = name[1:].replace(' ','_').split()[0]
        if name == 'Error':
            log.error("Couldn't download page, aborting...")
            exit (25)

        open('{}/problem.html'.format(db_folder,code),'a').write(str(soup))
