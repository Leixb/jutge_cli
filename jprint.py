#!/usr/bin/python3

import logging
log = logging.getLogger('jutge.jprint')

from os.path import expanduser
from glob import glob

import jgetcode
import jdownload

from bs4 import BeautifulSoup

class jprint:
    def __init__(self,args):
        code = jgetcode.jgetcode(args).code

        jdownload.jdownload(args) # Download problem.html if necessary

        html = open('{}/{}/problem.html'.format(expanduser(args.database),code),'r')
        soup = BeautifulSoup(html,'lxml')
        self.title = "-".join(soup.find('title').text.split('-')[1:])
        self.title = self.title[1:].replace(' ','_').split()[0]

        try:
            if args.mode == 'title': print(self.title)
            elif args.mode == 'stat':
                import pypandoc
                # Find statements in html. First paragraph removed cause it contains junk
                txt = soup.find('div',id="txt").find_all('p')[1:] 

                # Merge into a plain html string
                txt = " ".join([str(i) for i in txt])

                # Convert html to plain text using pandoc
                txt = pypandoc.convert_text(txt,'plain','html')
                print(self.title + '\n')
                print(txt)

            elif args.mode == 'cases':
                cont = 0
                for sample_inp in sorted(glob('{}/{}/*.{}'.format(expanduser(args.database),code,args.inp_suffix))):
                    sample_cor = ''.join(sample_inp.split('.')[:-1]) + '.' + args.cor_suffix

                    cont+=1

                    print('### Input {}'.format(cont))
                    print(open(sample_inp,'r').read())
                    print('### Output {}'.format(cont))
                    print(open(sample_cor,'r').read())
        except AttributeError:
            pass
