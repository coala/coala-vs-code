import json


def output_to_diagnostics(output):
    """
    Turn output to diagnstics.
    """
    if output is None:
        return None
    output_json = json.loads(output)['results']
    res = []
    for key, problems in output_json.items():
        section = key
        for problem in problems:
            """
            Transform RESULT_SEVERITY of coala into DiagnosticSeverity of LSP
            coala: INFO = 0, NORMAL = 1, MAJOR = 2
            LSP: Error = 1, Warning = 2, Information = 3, Hint = 4
            """
            severity = 3 - problem['severity']
            message = problem['message']
            origin = problem['origin']
            real_message = '[{}] {}: {}'.format(section, origin, message)
            for code in problem['affected_code']:
                """
                Line position and character offset should be zero-based
                according to LSP, but row and column positions of coala
                are None or one-based number.
                coala uses None for convenience. None for column means the
                whole line while None for line means the whole file.
                """
                def convert_offset(x): return x - 1 if x else x
                start_line = convert_offset(code['start']['line'])
                start_char = convert_offset(code['start']['column'])
                end_line = convert_offset(code['end']['line'])
                end_char = convert_offset(code['end']['column'])
                if start_char is None or end_char is None:
                    start_char = 0
                    end_line = start_line + 1
                    end_char = 0
                res.append({
                    'severity': severity,
                    'range': {
                        'start': {
                            'line': start_line,
                            'character': start_char
                        },
                        'end': {
                            'line': end_line,
                            'character': end_char
                        }
                    },
                    'source': 'coala',
                    'message': real_message
                })
    return res
