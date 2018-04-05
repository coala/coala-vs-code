import os
import unittest

from coala_langserver.diagnostic import output_to_diagnostics


def get_output(filename):
    file_path = os.path.join(os.path.dirname(__file__),
                             'resources/diagnostic',
                             filename)
    with open(file_path, 'r') as file:
        output = file.read()
    return output


class DiagnosticTestCase(unittest.TestCase):

    def test_none_output(self):
        result = output_to_diagnostics(None)
        self.assertEqual(result, None)

    def test_severity_info(self):
        output = get_output('output_severity_info.json')
        result = output_to_diagnostics(output)

        # INFO: 0 (coala) -> Information: 3 (LSP)
        self.assertEqual(result[0]['severity'], 3)

    def test_severity_normal(self):
        output = get_output('output_severity_normal.json')
        result = output_to_diagnostics(output)

        # NORMAL: 1 (coala) -> Warning: 2 (LSP)
        self.assertEqual(result[0]['severity'], 2)

    def test_severity_major(self):
        output = get_output('output_severity_major.json')
        result = output_to_diagnostics(output)

        # MAJOR: 2 (coala) -> Error: 1 (LSP)
        self.assertEqual(result[0]['severity'], 1)

    def test_char_none(self):
        output = get_output('output_char_none.json')
        result = output_to_diagnostics(output)

        # None column should be regarded as the whole line
        start_line = result[0]['range']['start']['line']
        start_char = result[0]['range']['start']['character']
        end_line = result[0]['range']['end']['line']
        end_char = result[0]['range']['end']['character']
        self.assertEqual(start_char, 0)
        self.assertEqual(end_char, 0)
        self.assertEqual(start_line + 1, end_line)

    def test_normal_offset(self):
        output = get_output('output_normal_offset.json')
        result = output_to_diagnostics(output)

        # normal offset, one-based -> zero-based
        start_line = result[0]['range']['start']['line']
        start_char = result[0]['range']['start']['character']
        end_line = result[0]['range']['end']['line']
        end_char = result[0]['range']['end']['character']
        self.assertEqual(start_char, 0)
        self.assertEqual(end_char, 1)
        self.assertEqual(start_line, 0)
        self.assertEqual(end_line, 0)

    def test_multiple_problems(self):
        output = get_output('output_multiple_problems.json')
        result = output_to_diagnostics(output)

        # should be able to handle multiple bears & problems
        self.assertEqual(len(result), 3)
