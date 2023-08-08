#!/usr/bin/python3
import io
import os
from beamline_monitor.version import __version__

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'beamline_monitor'
DESCRIPTION = 'Small utility to monitor beamline status'
EMAIL = 'yury.matveev@desy.de'
AUTHOR = 'Yury Matveyev'
REQUIRES_PYTHON = '>=3.7'

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {'__version__': __version__}

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_dir={'beamline_monitor': 'beamline_monitor',},
    package_data={'beamline_monitor': ['beamline_monitor/*.py',
                                       'beamline_monitor/default_settings.ini',
                                       'beamline_monitor/gui/*.py',
                                       'beamline_monitor/resources/*.mp3'],},
    include_package_data=True,
    license='GPLv3',
    entry_points={'console_scripts': ['beamline_monitor = beamline_monitor:main',],},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable'
    ],
)
