#!/usr/bin/env python3

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='jutge_cli',
        version='1.5.6',

        description='CLI to manage jutge.org problems',
        long_description=long_description,

        url='http://github.com/Leixb/jutge_cli',

        author='Aleix Boné (Leix_b)',
        author_email='abone9999@gmail.com',

        license='GPL3',

        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU GPLv3',
            'Programming Language :: Python :: 3',
            ],

        keywords='',

        packages=['jutge_cli','jutge_cli.commands'],

        install_requires=[
            'pypandoc',
            'requests',
            'bs4',
            'argparse',
            'pyyaml'
            ],

        entry_points = {
            'console_scripts': ['jutge=jutge_cli.jutge:main'],
            },

        zip_safe=False
        )
