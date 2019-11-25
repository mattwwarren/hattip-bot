#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages
from hattip import __version__


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='hattip-bot',
    version=__version__,
    author='mattwwarren',
    author_email='matt@warrencomputing.net',
    license='MIT',
    url='https://github.com/mattwwarren/hattip-bot',
    description='Slack bot for giving a co-worker a tip of your hat!',
    # TODO: long_description=read('README.rst'),
    packages=find_packages(exclude=['tests']),
    python_requires='~=3.7',
    install_requires=[
        'aiohttp>=3.6',
        'slackclient>=2.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
    },
)
