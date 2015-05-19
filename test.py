from flake8_print import check_code_for_print_statements, PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE
from nose.tools import assert_equal, assert_true


# Python 3 detects the col as the column with the execution brackets rather than the function name. So we will attempt both when necessary.


class Flake8PrintTestCases(object):
    def generate_error_statement(self, line, col):
        return ['{}:{}:{} {} {}'.format('test.py', line, col, PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE)]


class TestGenericCases(Flake8PrintTestCases):
    def test_skips_noqa(self):
        result = check_code_for_print_statements('print(4) # noqa')
        assert_equal(result, list())

    def test_skips_noqa_line_only(self):
        result = check_code_for_print_statements('print(4) # noqa\nprint(5)\n # noqa')
        try:
            assert_equal(result, [{'col': 0, 'line': 2, 'message': 'T001 print statement found.'}])
        except AssertionError:
            assert_equal(result, [{'col': 5, 'line': 2, 'message': 'T001 print statement found.'}])

    def test_catches_simple_print_python2(self):
        try:
            result = check_code_for_print_statements('print 4')
            assert_equal(result, [{'col': 0, 'line': 1, 'message': 'T001 print statement found.'}])
        except SyntaxError:
            from sys import version
            assert_true(float(version[:3]) >= 3.0)

    def test_catches_simple_print_python3(self):
        result = check_code_for_print_statements('print(4)')
        try:
            assert_equal(result, [{'col': 0, 'line': 1, 'message': 'T001 print statement found.'}])
        except AssertionError:
            assert_equal(result, [{'col': 5, 'line': 1, 'message': 'T001 print statement found.'}])


class TestComments(Flake8PrintTestCases):
    def test_print_in_inline_comment_is_not_a_false_positive(self):
        result = check_code_for_print_statements('# what should I print ?')
        assert_equal(result, list())

    def test_print_same_line_as_comment(self):
        result = check_code_for_print_statements('print(5) # what should I do with 5 ?')
        try:
            assert_equal(result, [{'col': 0, 'line': 1, 'message': 'T001 print statement found.'}])
        except AssertionError:
            assert_equal(result, [{'col': 5, 'line': 1, 'message': 'T001 print statement found.'}])


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


class MultilineFlasePositive(Flake8PrintTestCases):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('hello="""there is a \nprint on\n the next line"""')
        assert_equal(result, list())

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_code_for_print_statements('a("""print the things""", 25)')
        assert_equal(result, list())
