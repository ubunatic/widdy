[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ubunatic)

widdy
=====

Widdy widdy widgets for rapid prototyping of [urwid](http://urwid.org) based console apps.

Installation
------------

    pip install widdy

Usage
-----
Read the [examples](https://github.com/ubunatic/widdy/tree/master/widdy/examples)
or try the demo apps:

    widdy chuck     # chuck norris joke reader
    widdy counter   # fun with text tables
    widdy all       # run all available demos

Development
-----------
First clone the repo.

    git clone https://github.com/ubunatic/widdy
    cd widdy

Then install the cloned version and install missing tools.

    make             # clean and run all tests
    make install     # install the checked-out dev version
    make transpiled  # transpile Py3 to Py2

You may need to install some tools and modules, i.e., `flake8`, `pytest-3`, `twine`, `urwid`, and maybe others.

[Pull requests](https://github.com/ubunatic/widdy/pulls) are welcome!
