#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from setuptools import setup, find_packages

setup(name='ODBPy',
      version='0.1',
      description='ODB++ support for Python',
      author='Uli Köhler',
      author_email='ukoehler@techoverflow.net',
      url='https://techoverflow.net/',
      license='Apache License v2.0',
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      requires=[],
      test_suite='nose.collector',
      tests_require=['nose', 'coverage', 'mock', 'rednose', 'nose-parameterized'],
      setup_requires=['nose>=1.0'],
      platforms="any",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Information Technology',
        'License :: DFSG approved',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
      ]
)
