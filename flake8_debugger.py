import pep8
import re

__version__ = '1.0'

DEBUGGER_REGEX = re.compile(r'(import i?pdb|i?pdb.set_trace())')

def check_for_debugger(line_of_code):
    if pep8.noqa(line_of_code):
        return
    debug_match = DEBUGGER_REGEX.search(line_of_code)
    if debug_match:
        return debug_match.start(), 'T000 pdb/ipdb found.'

check_for_debugger.name = name = 'flake8-debugger'
check_for_debugger.version = __version__
