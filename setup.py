#!/usr/bin/env python

"""
Flask-Mixer
-----------

Object generation for Flask and SQLAlchemy.

"""

import os
from sys import version_info

from setuptools import setup, find_packages

from flask_mixer import __version__, __project__, __license__


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


install_requires = ['Flask>=0.8', 'Flask-SQLAlchemy>=0.16']
if version_info < (2, 7):
    install_requires.append('importlib')


META_DATA = dict(
    name=__project__,
    version=__version__,
    license=__license__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/Flask-Milkman',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    packages=find_packages(),
    install_requires=install_requires,
    test_suite = 'tests',
)


if __name__ == "__main__":
    setup(**META_DATA)
