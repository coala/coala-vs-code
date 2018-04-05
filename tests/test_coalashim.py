import unittest
from unittest import mock

from coala_langserver.coalashim import run_coala_with_specific_file


def generate_side_effect(message, ret):
    def side_effect():
        print(message, end=''),
        return ret
    return side_effect


@mock.patch('coala_langserver.coalashim.log')
@mock.patch('coala_langserver.coalashim.coala')
class ShimTestCase(unittest.TestCase):

    def test_call(self, mock_coala, mock_log):
        mock_coala.return_value = 1
        run_coala_with_specific_file(None, None)

        # coala is called without arguments
        mock_coala.main.assert_called_with()

    def test_issue_with_result(self, mock_coala, mock_log):
        message = 'issue found'
        mock_coala.main.side_effect = generate_side_effect(message, 1)
        output = run_coala_with_specific_file(None, None)

        # log is message information
        mock_log.assert_called_with('Output =', message)
        # return value is issue message
        self.assertEqual(message, output)

    def test_issue_no_result(self, mock_coala, mock_log):
        message = ''
        mock_coala.main.side_effect = generate_side_effect(message, 1)
        output = run_coala_with_specific_file(None, None)

        # log is `no results` reminder
        mock_log.assert_called_with('No results for the file')
        # return value is empty string
        self.assertEqual(message, output)

    def test_no_issue(self, mock_coala, mock_log):
        message = 'no issue'
        mock_coala.main.side_effect = generate_side_effect(message, 0)
        output = run_coala_with_specific_file(None, None)

        # log is `no issue` reminder
        mock_log.assert_called_with('No issues found')
        # return value is None
        self.assertEqual(None, output)

    def test_coala_error(self, mock_coala, mock_log):
        message = 'fatal error'
        mock_coala.main.side_effect = generate_side_effect(message, -1)
        output = run_coala_with_specific_file(None, None)

        # log is `exit` reminder
        mock_log.assert_called_with('Exited with:', -1)
        # return value is None
        self.assertEqual(None, output)

    @mock.patch('coala_langserver.coalashim.os')
    def test_working_dir_normal(self, mock_os, mock_coala, mock_log):
        working_dir = '/'
        run_coala_with_specific_file(working_dir, None)
        mock_os.chdir.assert_called_with(working_dir)

    @mock.patch('coala_langserver.coalashim.os')
    def test_working_dir_none(self, mock_os, mock_coala, mock_log):
        working_dir = None
        run_coala_with_specific_file(working_dir, None)
        mock_os.chdir.assert_called_with('.')
