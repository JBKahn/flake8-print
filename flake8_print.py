"""Extension for flake8 that finds usage of print."""
import re

__version__ = '2.0.0'

PRINT_ERROR_CODE = 'T001'
PRINT_ERROR_MESSAGE = 'print statement found.'

RE_PRINT_STATEMENT = re.compile(r"(?<![=\s])\s*\bprint\b\s+[^(=]")
RE_PRINT_FUNCTION = re.compile(r"(?<!def\s)\bprint\b\s*\([^)]*\)")
RE_PRINT_NAME = re.compile(r"\bprint\b")


def print_usage(logical_line, noqa=None):
    if noqa:
        return
    m = RE_PRINT_STATEMENT.search(logical_line)
    if m:
        yield m.start(), '{0} {1}'.format(
            PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE)
        return

    m = RE_PRINT_FUNCTION.search(logical_line)
    if m:
        yield m.start(), '{0} {1}'.format(
            PRINT_ERROR_CODE, 'print function found.')
        return

    m = RE_PRINT_NAME.search(logical_line)
    if m:
        yield m.start(), 'T101 Python 2.x reserved word print used.'
