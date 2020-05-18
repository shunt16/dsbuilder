from io import open
from os import path

from setuptools import find_packages, setup

# Get package __version__.
# Same effect as "from s import __version__",
# but avoids importing the module which may not be installed yet:
__version__ = None
here = path.abspath(path.dirname(__file__))
with open('dsbuilder/version.py') as f:
    exec(f.read())

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='dsbuilder',
      version=__version__,
      description='',
      authors='',
      long_description=long_description,
      author_email='',
      url='',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[],
      entry_points={
          'console_scripts': [
          ],
                    }
      )
