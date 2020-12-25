#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='honeybee-radiance-pollination',
    author='mostapha',
    author_email='mostapha@ladybug.tools',
    setup_requires=['setuptools_scm'],
    packages=find_packages('honeybee_radiance_pollination'),
    keywords=['honeybee', 'radiance', 'ladybug-tools', 'daylight'],
    license='PolyForm Shield License 1.0.0'
)
