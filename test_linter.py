import pycodestyle

from textwrap import dedent

from flake8_print import PrintChecker


class CaptureReport(pycodestyle.BaseReport):
    """Collect the results of the checks."""

    def __init__(self, options):
        self._results = []
        super(CaptureReport, self).__init__(options)

    def error(self, line_number, offset, text, check):
        """Store each error."""
        code = super(CaptureReport, self).error(line_number, offset, text, check)
        if code:
            record = {"line": line_number, "col": offset, "message": "{0} {1}".format(code, text[5:])}
            self._results.append(record)
        return code


class PrintTestStyleGuide(pycodestyle.StyleGuide):

    logical_checks = []
    physical_checks = []
    ast_checks = [("print_usage", PrintChecker, ["tree", "filename", "lines"])]
    max_line_length = None
    hang_closing = False
    verbose = False
    benchmark_keys = {"files": 0, "physical lines": 0, "logical lines": 0}
    max_doc_length = None
    indent_size = 4


_print_test_style = PrintTestStyleGuide()


def check_code_for_print_statements(code):
    """Process code using pycodestyle Checker and return all errors."""
    from tempfile import NamedTemporaryFile

    test_file = NamedTemporaryFile(delete=False)
    test_file.write(code.encode())
    test_file.flush()
    report = CaptureReport(options=_print_test_style)
    lines = [line + "\n" for line in code.split("\n")]
    checker = pycodestyle.Checker(filename=test_file.name, lines=lines, options=_print_test_style, report=report)

    checker.check_all()
    return report._results


T201 = "T201 print found."
T203 = "T203 pprint found."
T202 = "T202 Python 2.x reserved word print used."
T204 = "T204 pprint declared."


class TestGenericCases(object):
    def test_catches_multiline_print(self):
        result = check_code_for_print_statements(
            dedent(
                """
            print("a"
                  "b")
        """
            )
        )
        assert result == [{"col": 0, "line": 2, "message": T201}]

    def test_catches_simple_print_python3(self):
        result = check_code_for_print_statements("print(4)")
        assert result == [{"col": 0, "line": 1, "message": T201}]

    def test_catches_pprint(self):
        result = check_code_for_print_statements("pprint(4)")
        assert result == [{"col": 0, "line": 1, "message": T203}]

    def test_catches_print_multiline(self):
        result = check_code_for_print_statements("print(0\n)")
        assert result == [{"col": 0, "line": 1, "message": T201}]

    def test_catches_empty_print(self):
        result = check_code_for_print_statements("print(\n)")
        assert result == [{"col": 0, "line": 1, "message": T201}]

    def test_catches_print_invocation_in_lambda(self):
        result = check_code_for_print_statements("x = lambda a: print(a)")
        assert result == [{"col": 14, "line": 1, "message": T201}]


class TestComments(object):
    def test_print_in_inline_comment_is_not_a_false_positive(self):
        result = check_code_for_print_statements("# what should I print ?")
        assert result == list()

    def test_print_same_line_as_comment(self):
        result = check_code_for_print_statements("print(5) # what should I do with 5 ?")
        assert result == [{"col": 0, "line": 1, "message": T201}]


class TestSingleQuotes(object):
    def test_print_in_one_single_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements("a('print the things', 25)")
        assert result == list()

    def test_print_in_three_single_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements("a('''print the things''', 25)")
        assert result == list()


class TestDoubleQuotes(object):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("print the things", 25)')
        assert result == list()

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("""print the things""", 25)')
        assert result == list()


class TestMultilineFalsePositive(object):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('hello="""there is a \nprint on\n the next line"""')
        assert result == list()

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("""print the things""", 25)')
        assert result == list()


class TestNameFalsePositive(object):
    def test_print_in_name(self):
        result = check_code_for_print_statements("def print_foo(): pass")
        assert result == []
        result = check_code_for_print_statements("def foo_print(): pass")
        assert result == []
        result = check_code_for_print_statements("foo_print = 1")
        assert result == []
        result = check_code_for_print_statements("print_foo = 1")
        assert result == []

    def test_redefine_print_function(self):
        result = check_code_for_print_statements("def print(): pass")
        assert result == [{"col": 0, "line": 1, "message": T202}]

    def test_print_arg(self):
        result = check_code_for_print_statements("def foo(print): pass")
        assert result == [{"col": 0, "line": 1, "message": T202}]

        result = check_code_for_print_statements("def foo(*, print=3): pass")
        assert result == [{"col": 0, "line": 1, "message": T202}]

        result = check_code_for_print_statements("def foo(print=3): pass")
        assert result == [{"col": 0, "line": 1, "message": T202}]

    def test_print_assignment(self):
        result = check_code_for_print_statements("print=1")
        assert result == [{"col": 0, "line": 1, "message": T202}]

    def test_print_assignment_value(self):
        result = check_code_for_print_statements("x = print")
        assert result == [{"col": 4, "line": 1, "message": T202}]

    def test_print_assignment_value_else(self):
        result = check_code_for_print_statements("x = print if True else 1")
        assert result == [{"col": 4, "line": 1, "message": T202}]
        result = check_code_for_print_statements("x = 1 if True else print")
        assert result == [{"col": 19, "line": 1, "message": T202}]

    def test_print_assignment_value_or(self):
        result = check_code_for_print_statements("x = print or 1")
        assert result == [{"col": 4, "line": 1, "message": T202}]
        result = check_code_for_print_statements("x = 1 or print")
        assert result == [{"col": 9, "line": 1, "message": T202}]

    def test_print_in_lambda(self):
        result = check_code_for_print_statements("x = lambda a: print")
        assert result == [{"col": 14, "line": 1, "message": T202}]


class TestPprintCases(object):
    def test_pprint_module_ignored(self):
        result = check_code_for_print_statements("import pprint;")
        assert result == list()

    def test_pprint_function_ignored(self):
        result = check_code_for_print_statements("import pprint; pprint.pprint;")
        assert result == list()

    def test_pprint_function_call_detected(self):
        result = check_code_for_print_statements('import pprint; pprint.pprint("foo");')
        assert result == [{"col": 15, "line": 1, "message": T203}]

    def test_pprint_standalone_function_call_detected(self):
        result = check_code_for_print_statements('from pprint import pprint; pprint("foo");')
        assert result == [{"col": 27, "line": 1, "message": T203}]

    def test_pprint_function_call_with_complex_data(self):
        result = check_code_for_print_statements('import pprint; pprint.pprint({"foo": "print"});')
        assert result == [{"col": 15, "line": 1, "message": T203}]
