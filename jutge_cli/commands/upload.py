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

from glob import glob
from logging import getLogger
from time import sleep

from bs4 import BeautifulSoup
from requests import get, post

from .check_submissions import check_last, check_problem
from . import test

LOG = getLogger('jutge.upload')


def upload(prog, problem_set, problem_sets, delay=100,
           no_skip_accepted=False, **kwargs):
    """
    :param prog:
    :param problem_set:
    :param problem_sets:
    :param delay:
    :param no_skip_accepted:
    """

    if problem_set:
        set_name = prog
        try:
            problems = problem_sets[set_name]
        except KeyError:
            LOG.error('Problem set not found')
            exit(20)
    else:
        upload_problem(prog, **kwargs)
        exit(0)

    LOG.debug(problems)

    submit_queue = []

    for subcode in problems:

        files = glob('{}*[!.x]'.format(subcode))\
                + glob('{}/{}*[!.x]'.format(set_name, subcode))
        if files:
            if not no_skip_accepted:

                veredict = check_problem(subcode, **kwargs)
                LOG.debug('%s %s', subcode, veredict)

                if veredict == 'accepted':
                    continue

            submit_queue += [files[0]]

        else:
            LOG.warning(subcode + ' solution not found, skiping ...')

    LOG.debug(submit_queue)

    if len(submit_queue) > 10:
        print('Submit queue contains {} elements, continue? [Ny]'.format(
            len(submit_queue)))
        if not input().lower() in ('y', 'ye', 'yes'):
            exit(130)

    for problem in submit_queue:
        upload_problem(prog=problem, **kwargs)

        sleep(delay/1000.0)

def upload_problem(prog, code, cookies, compiler, check=True,
                   no_download=False, skip_test=False, quiet=False, **kwargs):
    """
    :param prog:
    :param cookies:
    :param compiler:
    :param check:
    :param no_download:
    :param skip_test:
    :param quiet:
    """
    if no_download:
        LOG.error('Remove --no-download flag to upload')
        exit(4)

    if not skip_test:
        veredict = test.test(prog=prog, code=code, no_custom=True,
                             cookies=cookies, quiet=True, **kwargs)
        if veredict != 0:
            LOG.error('Problem did not pass public tests, aborting... \
(use --skip-test to upload anyways)')
            exit(veredict)
        else:
            LOG.debug('Public tests passed')

    web = 'https://jutge.org/problems/{}/submissions'.format(code)
    LOG.debug(web)

    # We need token_uid for POST to work
    response = get(web, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')

    token_uid = soup.find('input', {'name' : 'token_uid'})['value']
    LOG.debug(token_uid)

    extension = prog.split('.')[-1]  # To determine compiler

    compilers = dict(
        ada='GNAT',
        bas='FBC',
        bf='BEEF',
        c='GCC',
        cc='P1++',
        cpp='G++11',
        cs='MonoCS',
        d='GDC',
        erl='Erlang',
        f='GFortran',
        go='Go',
        hs='GHC',
        java='JDK',
        js='nodejs',
        lisp='CLISP',
        lua='Lua',
        m='GObjC',
        pas='FPC',
        php='PHP',
        pl='Perl',
        py='Python3',
        py2='Python',
        r='R',
        rb='Ruby',
        scm='Chicken',
        v='Verilog',
        ws='WS',
    )

    if compiler is not None:
        compilers[extension] = compiler

    data = {
        'annotation' : 'Uploaded by jutge_cli',
        'compiler_id' : compilers[extension],
        'submit' : 'submit',
        'token_uid' : token_uid
        }

    LOG.debug(data)

    with open(prog, 'r') as prog_file:
        files = {
            'file' : ['{}.{}'.format(code, extension), prog_file]
            }

        if check:
            prev_veredict = check_last(cookies=cookies, quiet=True)

        post(web, data=data, files=files, cookies=cookies)

    if check:
        for _ in range(0, 6):
            sleep(5)
            veredict = check_last(cookies=cookies, quiet=True)
            LOG.debug(veredict)
            if prev_veredict['time'] != veredict['time'] \
                    and veredict['code'] == code:
                if veredict['veredict'] == 'Pending':
                    continue
                else:
                    if not quiet:
                        print(veredict['veredict'])
                    if veredict['veredict'] in ('AC', '100/100'):
                        exit(0)
                    else:
                        exit(1)
        LOG.error('Check timed out')
        exit(2)

