#!/usr/bin/env python

import os
import re
import sys
import codecs

from setuptools import setup, find_packages

def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-birthday',
    version=find_version('birthday', '__init__.py'),
    license='BSD License',

    install_requires=[
    ],
    requires=[
        'Django (>=1.4.2)',
    ],

    description = 'Helper field and manager for working with birthdays',
    long_description=read('README.rst'),

    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',

    maintainer ='Basil Shubin',
    maintainer_email='basil.shubin@gmail.com',

    url='https://github.com/bashu/django-birthday',
    download_url='https://github.com/bashu/django-birthday/zipball/master',

    packages=find_packages(exclude=('example*', '*.tests*')),
    include_package_data=True,

    tests_require=[
        'django-setuptest',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
