import sys
import os
import io
from contextlib import redirect_stdout

from coalib import coala

from .log import log


def run_coala_with_specific_file(working_dir, file):
    sys.argv = ['', '--json', '--find-config', '--limit-files', file]
    if working_dir is None:
        working_dir = '.'
    os.chdir(working_dir)
    f = io.StringIO()
    with redirect_stdout(f):
        retval = coala.main()
    output = None
    if retval == 1:
        output = f.getvalue()
        if output:
            log('Output =', output)
        else:
            log('No results for the file')
    elif retval == 0:
        log('No issues found')
    else:
        log('Exited with:', retval)
    return output
