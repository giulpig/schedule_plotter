# -*- coding: utf-8 -*-
"""
    setup.py
    setup file for the library
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from setuptools import find_packages, setup

setup(
    name='schedule_plotter',
    url='https://github.com/giulpig/schedule_plotter',
    packages=find_packages(include=['schedule_plotter', 'schedule_plotter.*']),
    version='0.1.0',
    description='A tool to plot scheduling algorithms',
    author='giulpig',
    license='GPLv3',
    install_requires=["matplotlib", "sortedcontainers"],
    setup_requires=[]
)