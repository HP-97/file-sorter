import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='file-sorter',
    version='1.0',
    py_modules=['file-sorter'],
    install_requires=['pyyaml', 'watchdog'],
    description='Python script using the Watchdog API to sort files'
    )