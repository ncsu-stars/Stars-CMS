#!/usr/bin/env python

import os
from distutils.core import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(name='STARS CMS',
    version='1.0.1b1',
    author='NCSU STARS',
    author_email='',
    url='https://github.com/ncsu-stars/Stars-CMS/',
    license='BSD',
    description='CMS written in Python/Django specifically for STARS SLC\'s',
    packages=find_packages(exclude=['ncsu', 'project']),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.rst'),
    zip_safe=False,  # because we're including media that Django needs
)
