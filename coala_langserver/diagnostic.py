import json


def output_to_diagnostics(output):
    '""Turn output to diagnstics.""'
    if output is None:
        return None
    output_json = json.loads(output)['results']
    res = []
    for key, problems in output_json.items():
        section = key
        for problem in problems:
            severity = problem['severity']
            message = problem['message']
            origin = problem['origin']
            real_message = '[{}] {}: {}'.format(section, origin, message)
            for code in problem['affected_code']:
                res.append({
                    'severity': severity,
                    'range': {
                        'start': {
                            # Trick: VS Code starts from 0?
                            'line': code['start']['line'] - 1,
                            'character': code['start']['column']
                        },
                        'end': {
                            'line': code['end']['line'] - 1,
                            'character': code['end']['column']
                        }
                    },
                    'source': 'coala',
                    'message': real_message
                })
    return res
