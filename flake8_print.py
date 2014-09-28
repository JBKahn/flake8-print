import ast

__version__ = '1.3.0'

PRINT_ERROR_CODE = 'T001'
PRINT_ERROR_MESSAGE = 'print statement found.'


class PrintStatementChecker(object):
    name = 'flake8-print'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree

    def run(self):
        errors = check_tree_for_print_statements(self.tree)

        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def check_code_for_print_statements(code):
    tree = ast.parse(code)
    return check_tree_for_print_statements(tree)


def check_tree_for_print_statements(tree):
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Print):
            errors.append({
                "message": '{} {}'.format(PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE),
                "line": node.lineno,
                "col": node.col_offset
            })
    return errors
