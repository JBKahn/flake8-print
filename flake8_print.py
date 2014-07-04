import pep8
import re

__version__ = '1.2'

PRINT_REGEX = re.compile(r'(print)')
PRINT_ERROR_CODE = 'T001'
PRINT_ERROR_MESSAGE = 'print statement found.'


def check_for_print_statements(physical_line):
    if pep8.noqa(physical_line):
        return
    physical_line = re.sub(r'\"\"\"(.+?)\"\"\"', "", physical_line)
    physical_line = re.sub(r'\"(.+?)\"', "", physical_line)
    physical_line = re.sub(r'\'\'\'(.+?)\'\'\'', "", physical_line)
    physical_line = re.sub(r'\'(.+?)\'', "", physical_line)
    physical_line = re.sub(r'#(.+)', "#", physical_line)
    match = PRINT_REGEX.search(physical_line)
    if match:
        return match.start(), '{} {}'.format(PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE)


check_for_print_statements.name = name = 'flake8-print'
check_for_print_statements.version = __version__
