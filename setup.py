#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


required_packages=["pyyaml", "colorama"]


setup(
    name="micropype",
    version="0.1",
    packages=find_packages(),
    author="Bastien Cagna",
    description="Very basic pipelinning toolbox",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD 3',
    entry_points = {
        'console_scripts': ['segment_pnh = workflows.segment_pnh:main']},
    install_requires= required_packages,
    include_package_data=True)
