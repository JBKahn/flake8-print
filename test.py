import functools
import pycodestyle

from textwrap import dedent

from flake8_print import print_usage

try:
    from unittest import skipIf
except ImportError:
    skipIf = None

from nose.tools import assert_equal


class CaptureReport(pycodestyle.BaseReport):
    """Collect the results of the checks."""

    def __init__(self, options):
        self._results = []
        super(CaptureReport, self).__init__(options)

    def error(self, line_number, offset, text, check):
        """Store each error."""
        code = super(CaptureReport, self).error(line_number, offset,
                                                text, check)
        if code:
            record = {
                'line': line_number,
                'col': offset,
                'message': '{0} {1}'.format(code, text[5:]),
            }
            self._results.append(record)
        return code


class PrintTestStyleGuide(pycodestyle.StyleGuide):

    logical_checks = [
        ('print_usage', print_usage, ['logical_line', 'noqa']),
    ]
    physical_checks = []
    ast_checks = []
    max_line_length = None
    hang_closing = False
    verbose = False
    benchmark_keys = {'files': 0, 'physical lines': 0, 'logical lines': 0}


_print_test_style = PrintTestStyleGuide()

noqa_supported = hasattr(pycodestyle, 'noqa')

if not noqa_supported:
    # remove noqa
    _print_test_style.logical_checks[0] = (
        'print_usage', print_usage, ['logical_line'])


def check_code_for_print_statements(code):
    """Process code using pycodestyle Checker and return all errors."""
    report = CaptureReport(options=_print_test_style)
    lines = [line + '\n' for line in code.split('\n')]
    checker = pycodestyle.Checker(filename=None, lines=lines,
                           options=_print_test_style, report=report)

    checker.check_all()
    return report._results


class Flake8PrintTestCases(object):
    pass


if skipIf:
    skip_if_noqa_unsupported = functools.partial(
        skipIf,
        condition=not noqa_supported,
        reason='noqa is not supported on this flake8 version')
else:
    # Python 2.6 does not have skipIf or SkipTest, so
    # completely skip the test which will be reported as success.
    def skip_if_noqa_unsupported():
        """Decorator to unconditionally skip test method."""
        def noop(*args, **kwargs):
            pass

        return noop


T001 = 'T001 print statement found.'
T003 = 'T003 print function found.'
T101 = 'T101 Python 2.x reserved word print used.'


class TestNoQA(Flake8PrintTestCases):

    @skip_if_noqa_unsupported()
    def test_skips_noqa(self):
        result = check_code_for_print_statements('print(4) # noqa')
        assert_equal(result, list())

    @skip_if_noqa_unsupported()
    def test_skips_noqa_multiline_end(self):
        result = check_code_for_print_statements(dedent("""
            print("a"
                  "b")  # noqa
        """))
        assert_equal(result, list())

    @skip_if_noqa_unsupported()
    def test_skips_noqa_multiline_middle(self):
        result = check_code_for_print_statements(dedent("""
            print("a"
                  "b"  # noqa
                  "c")
        """))
        assert_equal(result, list())

    @skip_if_noqa_unsupported()
    def test_skips_noqa_multiline_start(self):
        result = check_code_for_print_statements(dedent("""
            print("a"  # noqa
                  "b")
        """))
        assert_equal(result, list())

    @skip_if_noqa_unsupported()
    def test_skips_noqa_line_only(self):
        result = check_code_for_print_statements('print(4); # noqa\nprint(5)\n # noqa')
        assert_equal(result, [{'col': 0, 'line': 2, 'message': T003}])


class TestGenericCases(Flake8PrintTestCases):

    def test_catches_multiline_print(self):
        result = check_code_for_print_statements(dedent("""
            print("a"
                  "b")
        """))
        assert_equal(result, [{'col': 0, 'line': 2, 'message': T003}])

    def test_catches_simple_print_python2(self):
        result = check_code_for_print_statements('print 4')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T001}])

    def test_catches_empty_print_python2(self):
        # TODO: This depends on __future__.print_function
        # as it can be either a print statement or unused function reference.
        result = check_code_for_print_statements('print')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T101}])

    def test_catches_simple_print_python3(self):
        result = check_code_for_print_statements('print(4)')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T003}])

    def test_catches_print_multiline(self):
        result = check_code_for_print_statements('print(0\n)')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T003}])

    def test_catches_empty_print(self):
        result = check_code_for_print_statements('print(\n)')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T003}])

    def test_catches_print_invocation_in_lambda(self):
        result = check_code_for_print_statements('x = lambda a: print(a)')
        assert_equal(result, [{'col': 14, 'line': 1, 'message': T003}])


class TestComments(Flake8PrintTestCases):
    def test_print_in_inline_comment_is_not_a_false_positive(self):
        result = check_code_for_print_statements('# what should I print ?')
        assert_equal(result, list())

    def test_print_same_line_as_comment(self):
        result = check_code_for_print_statements('print(5) # what should I do with 5 ?')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T003}])


class TestSingleQuotes(Flake8PrintTestCases):
    def test_print_in_one_single_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a(\'print the things\', 25)')
        assert_equal(result, list())

    def test_print_in_three_single_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a(\'\'\'print the things\'\'\', 25)')
        assert_equal(result, list())


class TestDoubleQuotes(Flake8PrintTestCases):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("print the things", 25)')
        assert_equal(result, list())

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("""print the things""", 25)')
        assert_equal(result, list())


class TestMultilineFalsePositive(Flake8PrintTestCases):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('hello="""there is a \nprint on\n the next line"""')
        assert_equal(result, list())

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("""print the things""", 25)')
        assert_equal(result, list())


class TestNameFalsePositive(Flake8PrintTestCases):

    def test_print_in_name(self):
        result = check_code_for_print_statements('def print_foo(): pass')
        assert_equal(result, [])
        result = check_code_for_print_statements('def foo_print(): pass')
        assert_equal(result, [])
        result = check_code_for_print_statements('foo_print = 1')
        assert_equal(result, [])
        result = check_code_for_print_statements('print_foo = 1')
        assert_equal(result, [])


class TestPython3NameFalsePositive(Flake8PrintTestCases):
    def test_redefine_print_function(self):
        result = check_code_for_print_statements('def print(): pass')
        assert_equal(result, [{'col': 4, 'line': 1, 'message': T101}])

    def test_print_method(self):
        result = check_code_for_print_statements(
            'class Foo: def print(self): pass')
        assert_equal(result, [{'col': 15, 'line': 1, 'message': T101}])

    def test_print_arg(self):
        result = check_code_for_print_statements('def foo(print): pass')
        assert_equal(result, [{'col': 8, 'line': 1, 'message': T101}])

    def test_print_assignment(self):
        result = check_code_for_print_statements('print=1')
        assert_equal(result, [{'col': 0, 'line': 1, 'message': T101}])

    def test_print_assignment_value(self):
        result = check_code_for_print_statements('x = print')
        assert_equal(result, [{'col': 4, 'line': 1, 'message': T101}])

    def test_print_assignment_value_else(self):
        result = check_code_for_print_statements('x = print if True else 1')
        assert_equal(result, [{'col': 4, 'line': 1, 'message': T101}])
        result = check_code_for_print_statements('x = 1 if True else print')
        assert_equal(result, [{'col': 19, 'line': 1, 'message': T101}])

    def test_print_assignment_value_or(self):
        result = check_code_for_print_statements('x = print or 1')
        assert_equal(result, [{'col': 4, 'line': 1, 'message': T101}])
        result = check_code_for_print_statements('x = 1 or print')
        assert_equal(result, [{'col': 9, 'line': 1, 'message': T101}])

    def test_print_in_lambda(self):
        result = check_code_for_print_statements('x = lambda a: print')
        assert_equal(result, [{'col': 14, 'line': 1, 'message': T101}])
