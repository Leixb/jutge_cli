#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.upload')

import requests
from bs4 import BeautifulSoup

from . import get_code

class upload:
    def __init__(self,args):

        if args.no_download:
            log.error('Remove --no-download flag to upload')
            exit(4)

        code = get_code.get_code(args).code
        log.debug(code)

        web = 'https://jutge.org/problems/{}/submissions'.format(code)
        log.debug(web)

        from . import cookie

        cookie_container = cookie.cookie(args)

        if cookie_container.has_cookie: cookies = dict(PHPSESSID=cookie_container.cookie)
        else:
            log.error("We need cookie to upload")
            exit(25)

        # We need token_uid for POST to work

        response = requests.get(web, cookies=cookies)
        soup = BeautifulSoup(response.text,'lxml')

        token_uid = soup.find('input', {'name' : 'token_uid'})['value']
        log.debug(token_uid)

        extension = args.prog.name.split('.')[-1] # To determine compiler

        compiler = dict(
                ada = 'GNAT',
                bas = 'FBC',
                bf = 'BEEF',
                c = 'GCC',
                cc = 'P1++',
                cpp = 'G++11',
                cs = 'MonoCS',
                d = 'GDC',
                erl = 'Erlang',
                f = 'GFortran',
                go = 'Go',
                hs = 'GHC',
                java = 'JDK',
                js = 'nodejs',
                lisp = 'CLISP',
                lua = 'Lua',
                m = 'GObjC',
                pas = 'FPC',
                php = 'PHP',
                pl = 'Perl',
                py = 'Python3',
                py2 = 'Python',
                r = 'R',
                rb = 'Ruby',
                scm = 'Chicken',
                v = 'Verilog',
                ws = 'WS',
                )

        if not args.compiler is None: compiler[extension] = args.compiler

        data = {
                'annotation' : 'Uploaded by jutge_cli', 
                'compiler_id' : compiler[extension], 
                'submit' : 'submit',
                'token_uid' : token_uid
                }

        log.debug(data)

        files= {
                'file' : open(args.prog.name,'r')
                }

        requests.post(web, data=data, files=files, cookies=cookies)

