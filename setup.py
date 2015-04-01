# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
WSGI app framework.

MapleTree is a micro-framework for web app development in Python.

See detail @ http://github.com/tomokinakamaru/mapletree.

Copyright (c) 2015, Tomoki Nakamaru.

License: MIT
"""

setup(
    author='Tomoki Nakamaru',
    author_email='tomoki.nakamaru@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='WSGI app framework',
    license='MIT',
    long_description=long_description,
    name='mapletree',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/mapletree',
    version='0.7.0',
)
