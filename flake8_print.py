import ast

__version__ = '1.3.0'

PRINT_ERROR_CODE = 'T001'
PRINT_ERROR_MESSAGE = 'print statement found.'


class PrintStatementChecker(object):
    name = 'flake8-print'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = filename

    def run(self):
        errors = list()
        with open(self.filename, 'r') as handle:
            errors = check_for_print_statements(handle.read(), self.filename)

        for error in errors:
            yield (error.line, 0, error.message, type(self))


def check_for_print_statements(code, filename):
    errors = []
    parsed = ast.parse(code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Print):
            print node.values[0].__dict__
            errors.append('{}:{}:{} {} {}'.format(filename, node.lineno, node.col_offset, PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE))
    return errors
