"""Honeybee Radiance plugin for Pollination."""
from .functions import *  # to make it easier to access the functions - not required

__queenbee__ = {
    'name': 'honeybee-radiance',
    'description': 'Honeybee Radiance plugin for Pollination.',
    'icon': 'https://raw.githubusercontent.com/ladybug-tools/artwork/master/icons_bugs/grasshopper_tabs/HB-Radiance.png',
    'home': 'https://ladybug.tools/honeybee-radiance/docs',
    'sources': [
        'https://github.com/ladybug-tools/honeybee-radiance',
        'https://hub.docker.com/r/ladybugtools/honeybee-radiance'
    ],
    'tag': '0.3.9',  # tag for honeybee-radiance plugin
    'app_version': '5.4',  # tag for version of Radiance
    'keywords': ['honeybee', 'radiance', 'ladybug-tools', 'daylight'],
    'maintainers': [
        {'name': 'mostapha', 'email': 'mostapha@ladybug.tools'}
    ],
    'license': {
        'name': 'PolyForm Shield License 1.0.0',
        'url': 'https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt'
    },
    'config': {
        'docker': {
            'image': 'ladybugtools/honeybee-radiance:1.27.21',
            'workdir': '/home/ladybugbot/run'
        }
    }
}
