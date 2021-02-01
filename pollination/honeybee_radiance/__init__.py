"""Honeybee Radiance plugin for Pollination."""

__queenbee__ = {
    'name': 'honeybee-radiance',  # name for queenbee package - this will overwrite the Python package name
    'icon': 'https://raw.githubusercontent.com/ladybug-tools/artwork/master/icons_bugs/grasshopper_tabs/HB-Radiance.png',
    'app_version': '5.4',  # tag for version of Radiance
    'config': {
        'docker': {
            'image': 'ladybugtools/honeybee-radiance:1.28.12',
            'workdir': '/home/ladybugbot/run'
        }
    }
}
