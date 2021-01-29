#!/usr/bin/env python
import setuptools
# add these line to integrate the queenbee packaging process into Python packaging
from queenbee_dsl.package import PackageQBInstall, PackageQBDevelop

with open("README.md", "r") as fh:
    long_description = fh.read()

# normal setuptool inputs
setuptools.setup(
    cmdclass={'develop': PackageQBDevelop, 'install': PackageQBInstall},    # this is critical for local packaging
    name='pollination-honeybee-radiance',                                   # will be used for package name unless it is overwritten using __queenbee__ info.
    setup_requires=['setuptools_scm'],
    version='0.4.0',                                                        # will be used as package tag
    url='https://github.com/pollination/pollination-honeybee-radiance',     # will be translated to home
    project_urls={
        'icon': 'https://raw.githubusercontent.com/ladybug-tools/artwork/master/icons_bugs/grasshopper_tabs/HB-Radiance.png',
        'docker': 'https://hub.docker.com/r/ladybugtools/honeybee-radiance'
    },
    description='Honeybee Radiance plugin for Pollination.',                # will be used as package description
    long_description=long_description,                                      # will be translated to ReadMe content on Pollination
    long_description_content_type="text/markdown",
    author='mostapha',                                                      # all the information for author and maintainers will be
    author_email='mostapha@ladybug.tools',                                  # translated to maintainers. For multiple authors use comma
    maintainer='ladybug-tools',                                             # inside the string.
    maintainer_email='info@ladybug.tools',
    packages=setuptools.find_packages('pollination_honeybee_radiance'),
    keywords='honeybee, radiance, ladybug-tools, daylight',                 # will be used as keywords
    license='PolyForm Shield License 1.0.0, https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt'  # the license link should be separated by a comma
)
