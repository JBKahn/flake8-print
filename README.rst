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

When both ``flake8 2.4.1`` and ``flake8-print`` are installed, the plugin is
available in ``flake8``::

    $ flake8 --version
    2.4.1 (pep8: 1.5.7, flake8-print: 2.0.0, mccabe: 0.3.1, pyflakes: 0.8.1)


Changes
-------

2.0 - 2015-11-10
````````````````
* Support noqa at end of multiline print statement
* Performance improvements
* Removed PrintStatementChecker class and other functions
* Added T101 for 'Python 2.x reserved word print used.'
* Added testing for Python 3.3 and 3.5, and different flake8 versions

1.6.1 - 2015-05-22
````````````````
* Fix bug introduced in 1.6.

1.6 - 2015-05-18
````````````````
* Added proper support for python3 and testing for python 2.6, 2.7 and 3.4

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
