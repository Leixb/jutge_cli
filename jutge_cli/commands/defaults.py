#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.defaults')

import yaml
from os.path import expanduser

class config:
    def __init__(self):

        try:
            with open(expanduser('~/.jutge_cli.yaml'),'r') as config_file:
                settings = yaml.load(config_file)
        except FileNotFoundError:
            log.warning('No config file round')
            settings = {}

        self.param = {}

        self.param['database'] = '~/Documents/jutge/DB'
        self.param['regex'] = '[PGQX]\d{5}_(ca|en|es)'
        self.param['diff-prog'] = 'diff'
        self.param['diff-flags'] = '-y'
        self.param['inp-suffix'] = 'inp'
        self.param['cor-suffix'] = 'cor'
        self.param['folder'] = '~/Documents/jutge/Done'

        self.subfolders = {}

        try: self.param['regex'] = settings['regex']
        except KeyError: pass
        try: self.param['database'] = settings['database']
        except KeyError: pass
        try: self.param['diff-prog'] = settings['diff-prog']
        except KeyError: pass
        try: self.param['diff-flags'] = settings['diff-flags']
        except KeyError: pass
        try: self.param['inp-suffix'] = settings['inp-suffix']
        except KeyError: pass
        try: self.param['cor-suffix'] = settings['cor-suffix']
        except KeyError: pass
        try: self.param['folder'] = settings['folder']
        except KeyError: pass
        try: self.subfolders = settings['problem_sets']
        except KeyError: pass

