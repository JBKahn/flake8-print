Flake8 print plugin
==================

Check for Print statements in python files.

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

Stdin
-----

Testing with `flake8==2.2.1`, and `2.2.4`. There was a bug in flake8 that was subsequently fixed.


Changes
-------

1.5 - 2014-11-04
````````````````
* Added python2.6 support. Thanks @zoidbergwill

1.4 - 2014-10-06
````````````````
* Apped noqa support

1.3 - 2014-09-27
````````````````
* Dropped noqa support
* Support for multiline comments and less false positives

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
