#!/usr/bin/python3

import configparser
from os.path import expanduser

class jconfig:
    def __init__(self):

        config_file = expanduser('~/.jutge_cli.conf')

        config = configparser.ConfigParser()
        config.read(config_file)

        self.param = {}

        self.param['database'] = '~/Documents/jutge/DB'
        self.param['regex'] = '[PGQX][0-9]{5}_(ca|en|es)'
        self.param['diff-prog'] = 'diff'
        self.param['diff-flags'] = '-y'
        self.param['inp-suffix'] = 'inp'
        self.param['cor-suffix'] = 'cor'
        self.param['folder'] = '~/Documents/jutge/Done'

        try: self.param['regex'] = config.get('DEFAULT', 'regex')
        except configparser.NoOptionError: pass
        try: self.param['database'] = config.get('DEFAULT', 'database')
        except configparser.NoOptionError: pass
        try: self.param['diff-prog'] = config.get('DEFAULT', 'diff-prog')
        except configparser.NoOptionError: pass
        try: self.param['diff-flags'] = config.get('DEFAULT', 'diff-flags')
        except configparser.NoOptionError: pass
        try: self.param['inp-suffix'] = config.get('DEFAULT', 'inp-suffix')
        except configparser.NoOptionError: pass
        try: self.param['cor-suffix'] = config.get('DEFAULT', 'cor-suffix')
        except configparser.NoOptionError: pass
        try: self.param['folder'] = config.get('DEFAULT', 'folder')
        except configparser.NoOptionError: pass
