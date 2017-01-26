import json


class Diagnostic(object):
    """Diagnostic class for VS Code."""

    def __init__(self, severity, range, message, section, origin):
        self.severity = severity
        self.range = range
        self.message = message
        self.source = "coala"
        self.section = section
        self.origin = origin
        self.real_message = self.make_real_message()

    def make_real_message(self):
        return "[{}] {}: {}".format(self.section, self.origin, self.message)


def output_to_diagnostics(output):
    """Turn output to diagnstics."""
    if output is None:
        return None
    output_json = json.loads(output)["results"]
    res = []
    for key, problems in output_json.items():
        section = key
        for problem in problems:
            severity = problem["severity"]
            message = problem["message"]
            origin = problem["origin"]
            real_message = "[{}] {}: {}".format(section, origin, message)
            for code in problem["affected_code"]:
                res.append({
                    "severity": severity,
                    "range": {
                        "start": {
                            # Trick: VS Code starts from 0?
                            "line": code["start"]["line"] - 1,
                            "character": code["start"]["column"]
                        },
                        "end": {
                            "line": code["end"]["line"] - 1,
                            "character": code["end"]["column"]
                        }
                    },
                    "source": "coala",
                    "message": real_message
                })
    return res
