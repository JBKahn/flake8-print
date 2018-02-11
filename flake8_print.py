"""Extension for flake8 that finds usage of print."""
import pycodestyle
import ast
from six import PY2, PY3

__version__ = '3.1.0'

PRINT_FUNCTION_NAME = "print"
PPRINT_FUNCTION_NAME = "pprint"
PRINT_FUNCTION_NAMES = [PRINT_FUNCTION_NAME, PPRINT_FUNCTION_NAME]

VIOLATIONS = {
    'found': {
        'print': 'T001 print found.',
        'pprint': 'T003 pprint found.',
    },
    'declared': {
        'print': 'T002 Python 2.x reserved word print used.',
        'pprint': 'T004 pprint declared',
    },
}


class PrintFinder(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super(PrintFinder, self).__init__(*args, **kwargs)
        self.prints_used = {}
        self.prints_redefined = {}

    def visit_Print(self, node):
        """Only exists in python 2."""
        self.prints_used[(node.lineno, node.col_offset)] = VIOLATIONS["found"][PRINT_FUNCTION_NAME]

    def visit_Call(self, node):
        is_print_function = getattr(node.func, "id", None) in PRINT_FUNCTION_NAMES
        is_print_function_attribute = (
            getattr(getattr(node.func, "value", None), "id", None) in PRINT_FUNCTION_NAMES and getattr(node.func, "attr", None) in PRINT_FUNCTION_NAMES
        )
        if is_print_function:
            self.prints_used[(node.lineno, node.col_offset)] = VIOLATIONS["found"][node.func.id]
        elif is_print_function_attribute:
            self.prints_used[(node.lineno, node.col_offset)] = VIOLATIONS["found"][node.func.attr]
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name in PRINT_FUNCTION_NAMES:
            self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][node.name]
        if PY2:
            for arg in node.args.args:
                if arg.id in PRINT_FUNCTION_NAMES:
                    self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][arg.id]
        elif PY3:
            for arg in node.args.args:
                if arg.arg in PRINT_FUNCTION_NAMES:
                    self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][arg.arg]

            for arg in node.args.kwonlyargs:
                if arg.arg in PRINT_FUNCTION_NAMES:
                    self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][arg.arg]
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id == PRINT_FUNCTION_NAME:
            self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][node.id]
        self.generic_visit(node)


class PrintChecker(object):
    options = None
    name = 'flake8-print'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    def run(self):
        if not self.tree or not self.lines:
            self.load_file()

        parser = PrintFinder()
        parser.visit(self.tree)
        for error, message in parser.prints_used.items():
            if not pycodestyle.noqa(self.lines[error[0] - 1]):
                yield (error[0], error[1], message, PrintChecker)

        for error, message in parser.prints_redefined.items():
            if error not in parser.prints_used:
                if not pycodestyle.noqa(self.lines[error[0] - 1]):
                    yield (error[0], error[1], message, PrintChecker)
