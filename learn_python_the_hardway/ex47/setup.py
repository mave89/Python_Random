try:
    from setuptools import setup
except ImportError
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Faiz Abidi',
    'url': 'URL to get it at.',
    'download_url': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ex47'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)