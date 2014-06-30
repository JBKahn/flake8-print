import pep8
import re

__version__ = '1.1'

PRINT_REGEX = re.compile(r'(print)')


def check_for_print_statements(physical_line):
    if pep8.noqa(physical_line):
        return
    match = PRINT_REGEX.search(physical_line)
    if match:
        return match.start(), 'T000 print statement found.'


check_for_print_statements.name = name = 'flake8-print'
check_for_print_statements.version = __version__
