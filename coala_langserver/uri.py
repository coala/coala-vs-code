import os


def path_from_uri(uri):
    '""Get the path from JSON RPC initialization request.""'
    if not uri.startswith('file://'):
        return uri
    _, path = uri.split('file://', 1)
    return path


def dir_from_uri(uri):
    '""Get the directory name from the path.""'
    return os.path.dirname(path_from_uri(uri))
