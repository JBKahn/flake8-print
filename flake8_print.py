"""Extension for flake8 that finds usage of print."""
import re

__version__ = '2.0.2'

CHECKS = [
    (re.compile(r"(?<![=\s])\s*\bprint\b\s+[^(=]"), 'T001', 'print statement found.'),
    (re.compile(r"(?<!def\s)\bprint\b\s*\([^)]*\)"), 'T003', 'print function found.'),
    (re.compile(r"\bprint\b"), 'T101', 'Python 2.x reserved word print used.')
]


def flake8ext(f):
    """Decorate flake8 extension function."""
    f.name = 'flake8-print'
    f.version = __version__
    return f


@flake8ext
def print_usage(logical_line, noqa=None):
    if noqa:
        return
    for regexp, code, message in CHECKS:
        match = regexp.search(logical_line)
        if match is not None:
            yield match.start(), '{0} {1}'.format(code, message)
            return
