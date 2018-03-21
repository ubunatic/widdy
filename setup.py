from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'README.md')) as f: readme = f.read()
readme = ""

setup(
    name             = 'ohlcwid',
    version          = '0.2.0',
    description      = 'urwid wrapper for rapid shell-ui prototyping',
    long_description = readme,
    url              = 'https://github.com/ubunatic/ohlcwid',
    author           = 'Uwe Jugel',
    author_email     = 'uwe.jugel@gmail.com',
    python_requires  = '>=3.5',
    # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        # 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console :: Curses',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'urwid prototyping widgets ohlc ui apps console',
    packages = find_packages(exclude=['contrib', 'docs', 'tests']),
    # see: https://packaging.python.org/en/latest/requirements.html
    install_requires = ['urwid','requests','asyncio'],  # html
    # example: pip install ohlcdev[dev]
    extras_require = {
        'dev': ['pytest','flake8'],
        # check-mainfest coverage
    },
    # data files
    # package_data={ 'sample': ['package_data.dat'] },
    # extern data files installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    entry_points = {  # Optional
        'console_scripts': [
            'ohlcwid-chuck=ohlcwid.examples.chuck:main',
            'ohlcwid-counter=ohlcwid.examples.counter:main',
        ],
    },
    # The key is used to render the link text on PyPI.
    project_urls = {
        'Documentation': 'https://github.com/ubunatic/ohlcwid',
        'Bug Reports':   'https://github.com/ubunatic/ohlcwid/issues',
        'Funding':       'https://github.com/ubunatic/ohlcwid',
        'Say Thanks!':   'https://saythanks.io/to/ubunatic',
        'Source':      '  https://github.com/ubunatic/ohlcwid',
    },
)

