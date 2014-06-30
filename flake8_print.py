import pep8
import re

__version__ = '1.0'

PRINT_REGEX = re.compile(r'(print)')

def check_for_print_statements(line_of_code):
    if pep8.noqa(line_of_code):
        return
    print_match = PRINT_REGEX.search(line_of_code)
    if print_match:
        return print_match.start(), 'T000 print statement found.'

check_for_print_statements.name = name = 'flake8-print'
check_for_print_statements.version = __version__
