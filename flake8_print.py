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
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def check_for_print_statements(code, filename):
    errors = []
    parsed = ast.parse(code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Print):
            errors.append({
                "message": '{} {}'.format(PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE),
                "line": node.lineno,
                "col": node.col_offset
            })
    return errors
