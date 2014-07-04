Flake8 print plugin
==================

Check for Print statements in python files. Currently gives false positives of doc strings and mult line strings. Lots of work to do.

This module provides a plugin for ``flake8``, the Python code checker.


Installation
------------

You can install or upgrade ``flake8-print`` with these commands::

  $ pip install flake8-print
  $ pip install --upgrade flake8-print


Plugin for Flake8
-----------------

When both ``flake8 2.2`` and ``flake8-print`` are installed, the plugin is
available in ``flake8``::

    $ flake8 --version
    2.0 (pep8: 1.4.5, flake8-print: 1.0, pyflakes: 0.6.1)


To Cover
------------

Cover multline comments and doc strings.


Changes
-------

1.2 - 2014-06-30
````````````````
* Does not catch the word print in single line strings
* Does not catch inline comments with print in it
* Added tests

1.1 - 2014-06-30
````````````````
* First release

1.0 - 2014-06-30
````````````````
* Whoops
