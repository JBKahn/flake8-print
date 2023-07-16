"""Extension for flake8 that finds usage of print."""
import pycodestyle
import ast

try:
    from flake8.engine import pep8 as stdin_utils
except ImportError:
    from flake8 import utils as stdin_utils

__version__ = "5.1.0"

PRINT_FUNCTION_NAME = "print"
PPRINT_FUNCTION_NAME = "pprint"
TRACEBACK_FUNCTION_NAMES = ["print_tb", "print_exception", "print_exc", "print_last", "print_stack"]
PRINT_FUNCTION_NAMES = [PRINT_FUNCTION_NAME, PPRINT_FUNCTION_NAME]

VIOLATIONS = {
    "found": {
        "print": "T201 print found.",
        "pprint": "T203 pprint found.",
    },
    "declared": {"print": "T202 Python 2.x reserved word print used.", "pprint": "T204 pprint declared"},
}

for func_name in TRACEBACK_FUNCTION_NAMES:
    VIOLATIONS["found"][func_name] = "T205 traceback print found."


class PrintFinder(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super(PrintFinder, self).__init__(*args, **kwargs)
        self.prints_used = {}
        self.prints_redefined = {}
        self.traceback_imports = []
        self.traceback_func_imports = {}

    def visit_Import(self, node: ast.Import):
        for import_ in node.names:
            if import_.name in ["traceback"] and hasattr(import_, "asname"):
                self.traceback_imports.append(import_.asname)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module in ["traceback"]:
            for import_ in node.names:
                if import_.asname:
                    self.traceback_func_imports[import_.asname] = import_.name
                else:
                    self.traceback_func_imports[import_.asname] = import_.name

    def visit_Call(self, node):
        is_print_function = (
            getattr(node.func, "id", None) in PRINT_FUNCTION_NAMES
            or getattr(node.func, "id", None) in self.traceback_func_imports
        )
        is_print_function_attribute = (
            getattr(getattr(node.func, "value", None), "id", None)
            in PRINT_FUNCTION_NAMES + ["traceback"] + self.traceback_imports
            and getattr(node.func, "attr", None) in PRINT_FUNCTION_NAMES + TRACEBACK_FUNCTION_NAMES
        )
        if is_print_function:
            func_name = node.func.id
        elif is_print_function_attribute:
            func_name = node.func.attr
        else:
            func_name = None
        if func_name in self.traceback_func_imports:
            func_name = self.traceback_func_imports[func_name]
        if func_name is not None:
            self.prints_used[(node.lineno, node.col_offset)] = VIOLATIONS["found"][func_name]
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name in PRINT_FUNCTION_NAMES:
            self.prints_redefined[(node.lineno, node.col_offset)] = VIOLATIONS["declared"][node.name]

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
    name = "flake8-print"
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = stdin_utils.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    def run(self):
        if not self.tree or not self.lines:
            self.load_file()

        parser = PrintFinder()
        parser.visit(self.tree)
        error_dicts = (parser.prints_used, parser.prints_redefined)
        errors_seen = set()

        for index, error_dict in enumerate(error_dicts):
            for error, message in error_dict.items():
                if error in errors_seen:
                    continue

                errors_seen.add(error)

                yield (error[0], error[1], message, PrintChecker)
