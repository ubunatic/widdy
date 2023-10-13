[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ubunatic)

widdy
=====

Widdy widdy widgets for rapid prototyping of [Urwid](http://urwid.org) based console apps.

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

You may need to install some tools and modules, i.e., `flake8`, `pytest-3`, `twine`, `urwid`, and maybe others.

[Pull requests](https://github.com/ubunatic/widdy/pulls) are welcome!

Project Status
--------------
The code and libs are usable but provide only limited features on top of [Urwid](http://urwid.org).
For small prototypes Widdy may make coding a bit easier. For bigger projects, use Urwid directly.

Updates are done very rarely (every few years actually), and only when I have a personal need for it.