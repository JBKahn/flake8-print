Flake8 print plugin
===================

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

Flake8 allows disabling some tests based on the folder:

```
[flake8]
per-file-ignores =
    scripts/*: T20
    cli.py: T20
```

Error codes
-----------

| Error Code  | Description                          |
| ----------- | ------------------------------------ |
| T201        | print found                          |
| T203        | pprint found                         |
| T204        | pprint declared                      |


Changes
-------

##### 5.0.0 - 2022-04-30

* Move namespace from T0* to T2* to avoid collision with other library using same error code.
* Remove python 2 specific code paths, error messages and six usage.

##### 4.0.1 - 2022-04-30

* Fixing bug with noqa detection by removing manual detection and relying on flake8 itself.

##### 4.0.0 - 2020-11-29

* Opted back into using Poetry now that the existing issues have been fixed.
* Python 2.7 support was now officially dropped.

##### 3.1.4 - 2019-1-11

* Fix bug introduced in 3.1.3
* Support for `nopep8` comments

##### 3.1.3 - 2019-31-10

* Swapped back from poetry to setup.py :(....python ecosystem issues....
* single function refactor code

##### 3.1.1 - 2019-03-12

* Fix reading from stdin when it is closed (requires flake8 > 2.1).
* Add error codes to ReadMe.
* Swapped to poetry from setup.py
* Ran black on the repository

##### 3.1.0 - 2018-02-11
* Add a framework classifier for use in pypi.org
* Fix entry_point in setup.py leaving it off by default again.

##### 3.0.1 - 2017-11-06
* Fix conflict in setup.py leaving it off by default again.
* Fix bug in name code.

##### 3.0.0 - 2017-11-05
* Remove some of the python 2/3 message differentiation.
* Use an AST rather than a logical line checker with a regex.
* pprint support.
* Loss of multiline noqa support, until there is a way to use both the AST and have flake8 provide the noqa lines.


##### 2.0.2 - 2016-02-29
* Fix ReadMe for pipy
* Refactor, DRY it up.
* Update python 2 vs python 3 print statement styles.

##### 2.0.1 - 2015-11-21
* Add back the decorator to fix the `flake8 --version` call.

##### 2.0 - 2015-11-10
* Support noqa at end of multiline print statement
* Performance improvements
* Removed PrintStatementChecker class and other functions
* Added T101 for 'Python 2.x reserved word print used.'
* Added testing for Python 3.3 and 3.5, and different flake8 versions

##### 1.6.1 - 2015-05-22
* Fix bug introduced in 1.6.

##### 1.6 - 2015-05-18
* Added proper support for python3 and testing for python 2.6, 2.7 and 3.4

##### 1.5 - 2014-11-04
* Added python2.6 support. Thanks @zoidbergwill

##### 1.4 - 2014-10-06
* Apped noqa support

##### 1.3 - 2014-09-27
* Dropped noqa support
* Support for multiline comments and less false positives

##### 1.2 - 2014-06-30
* Does not catch the word print in single line strings
* Does not catch inline comments with print in it
* Added tests

##### 1.1 - 2014-06-30
* First release

##### 1.0 - 2014-06-30
* Whoops
