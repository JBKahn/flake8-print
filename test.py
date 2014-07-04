from flake8_print import check_for_print_statements, PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE
from nose.tools import assert_equal


class Flake8PrintTestCases(object):
    def generate_error_statement(self, index):
        return (index, '{} {}'.format(PRINT_ERROR_CODE, PRINT_ERROR_MESSAGE))


class TestGenericCases(Flake8PrintTestCases):
    def test_skips_noqa(self):
        result = check_for_print_statements('44 print 4 # noqa')
        assert result is None

    def test_catches_simple_print_python2(self):
        result = check_for_print_statements('print 4')
        assert_equal(result, self.generate_error_statement(0))

    def test_catches_simple_print_python3(self):
        result = check_for_print_statements('print(4)')
        assert_equal(result, self.generate_error_statement(0))


class TestComments(Flake8PrintTestCases):
    def test_print_in_inline_comment_is_not_a_false_positive(self):
        result = check_for_print_statements('# what should I print ?')
        assert result is None

    def test_print_same_line_as_comment(self):
        result = check_for_print_statements('print 5 # what should I do with 5 ?')
        assert_equal(result, self.generate_error_statement(0))


class TestSingleQuotes(Flake8PrintTestCases):
    def test_print_in_one_single_quote_single_line_string_not_false_positive(self):
        result = check_for_print_statements('a(\'print the things\', 25)')
        assert result is None

    def test_print_in_between_two_one_single_quote_single_line_string(self):
        result = check_for_print_statements('a(\'print the things\' print \'print the things\', 25)')
        assert_equal(result, self.generate_error_statement(3))

    def test_print_in_three_single_quote_single_line_string_not_false_positive(self):
        result = check_for_print_statements('a(\'\'\'print the things\'\'\', 25)')
        assert result is None

    def test_print_in_between_two_three_single_quote_single_line_string(self):
        result = check_for_print_statements('a(\'\'\'print the things\'\'\' print \'\'\'print the things\'\'\', 25)')
        assert_equal(result, self.generate_error_statement(3))


class TestDoubleQuotes(Flake8PrintTestCases):
    def test_print_in_one_double_quote_single_line_string_not_false_positive(self):
        result = check_for_print_statements('a("print the things", 25)')
        assert result is None

    def test_print_in_between_two_one_double_quote_single_line_string(self):
        result = check_for_print_statements('a("print the things" print "print the things", 25)')
        assert_equal(result, self.generate_error_statement(3))

    def test_print_in_three_double_quote_single_line_string_not_false_positive(self):
        result = check_for_print_statements('a("""print the things""", 25)')
        assert result is None

    def test_print_in_between_two_three_double_quote_single_line_string(self):
        result = check_for_print_statements('a("print the things" print "print the things", 25)')
        assert_equal(result, self.generate_error_statement(3))
