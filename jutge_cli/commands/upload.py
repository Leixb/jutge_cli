#!/usr/bin/python3

# Copyright (C) 2017  Aleix Boné (abone9999 at gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import logging
log = logging.getLogger('jutge.upload')

import requests
from bs4 import BeautifulSoup

from os.path import expanduser
from glob import glob

from time import sleep

from . import get_code
from . import defaults
from . import test
from . import check_submissions

class upload:
    def __init__(self,args):
        config = defaults.config()
        if not args.skip_test:
            # Add defaults for test
            args_dict = vars(args)
            args_dict['inp_suffix'] = config.param['inp-suffix']
            args_dict['cor_suffix'] = config.param['cor-suffix']
            args_dict['diff_flags'] = config.param['diff-flags']
            args_dict['diff_prog']  = config.param['diff-prog']
            args_dict['no_custom']  = True
        if args.problem_set:
            set_name = args.prog
            try: problems = config.subfolders[set_name]
            except KeyError:
                log.error('Problem set not found')
                exit(20)

            args_dict = vars(args)

            log.debug(problems)

            submit_queue = []

            for subcode in problems:

                files = glob('{}*[!.x]'.format(subcode)) + glob('{}/{}*[!.x]'.format(set_name,subcode))
                if len(files) > 0: 
                    if not args.no_skip_accepted:

                        veredict = check_submissions.check_submissions(args).check_problem(subcode)
                        log.debug('{} {}'.format(subcode,veredict))

                        if veredict == 'accepted': continue

                    submit_queue += [files[0]]

                else: log.warning(subcode + ' solution not found, skiping ...')

            log.debug(submit_queue)

            if len(submit_queue) > 20:
                print('Submit queue contains more than 20 problems ({}) continue? [Ny]'.format(len(submit_queue)) )
                if not input().lower() in ('y','ye','yes'):
                    exit(130)
            elif len(submit_queue) > 10:
                print('Submit queue contains {} elements, continue? [Ny]'.format(len(submit_queue)))
                if not input().lower() in ('y','ye','yes'):
                    exit(130)

            for problem in submit_queue:

                args_dict['prog'] = problem
            
                self.upload(args)

                sleep(args.delay/1000.0)

        else: self.upload(args)

    def upload(self,args):
        if args.no_download:
            log.error('Remove --no-download flag to upload')
            exit(4)

        if not args.skip_test:
            veredict = test.test(args).eval()
            if veredict != 0:
                log.error('Problem did not pass public tests, aborting... (use --skip-test to upload anyways)')
                exit(veredict)
            else: log.debug('Public tests passed')

        code = get_code.get_code(args).code
        log.debug(code)

        web = 'https://jutge.org/problems/{}/submissions'.format(code)
        log.debug(web)

        from . import cookie

        cookie_container = cookie.cookie(args)

        if cookie_container.has_cookie: cookies = dict(PHPSESSID=cookie_container.cookie)
        else:
            log.error('We need cookie to upload')
            exit(25)

        if cookie_container.check_cookie() == None:
            log.error('Invalid cookie')
            exit(26)

        # We need token_uid for POST to work

        response = requests.get(web, cookies=cookies)
        soup = BeautifulSoup(response.text,'lxml')

        token_uid = soup.find('input', {'name' : 'token_uid'})['value']
        log.debug(token_uid)

        extension = args.prog.split('.')[-1] # To determine compiler

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
                'file' : [ '{}.{}'.format(code,extension)  , open(args.prog,'r')]
                }

        requests.post(web, data=data, files=files, cookies=cookies)

