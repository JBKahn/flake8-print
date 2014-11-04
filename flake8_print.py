import ast
import tokenize

from sys import stdin

__version__ = '1.5.0'

PRINT_ERROR_CODE = 'T001'
PRINT_ERROR_MESSAGE = 'print statement found.'


class PrintStatementChecker(object):
    name = 'flake8-print'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = (filename == 'stdin' and stdin) or filename

    def run(self):
        if self.filename == stdin:
            noqa = get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = get_noqa_lines(file_to_check.readlines())

        errors = check_tree_for_print_statements(self.tree, noqa)

        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def get_noqa_lines(code):
        tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
        noqa = [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
        return noqa


def check_code_for_print_statements(code):
    tree = ast.parse(code)
    noqa = get_noqa_lines(code.split("\n"))
    return check_tree_for_print_statements(tree, noqa)


def check_tree_for_print_statements(tree, noqa):
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Print) and node.lineno not in noqa:
            errors.append({
                "message": '{0} {1}'.format(PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE),
                "line": node.lineno,
                "col": node.col_offset
            })
    return errors
