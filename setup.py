#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-labyrinpy',
    version='0.1',
    description=' Django package for integration with Labyrintti SMS Gateway API',
    author='Magic Solutions',
    author_email='support@magicsolutions.bg',
    url='https://github.com/MagicSolutions/django-labyrinpy',
    packages=find_packages(exclude=("example_project",)),
    zip_safe=False,
    install_requires=['labyrinpy', 'Django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
