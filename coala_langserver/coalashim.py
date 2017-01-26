import subprocess
import tempfile

from .log import log


def run_coala_with_specific_file(working_dir, file):
    """Run coala in a specified directory."""
    command = ["coala", "--json", "--find-config", "--files", file]
    stdout_file = tempfile.TemporaryFile()
    kwargs = {"stdout": stdout_file,
              "cwd": working_dir}
    process = subprocess.Popen(command, **kwargs)
    retval = process.wait()
    output_str = None

    if retval == 1:
        stdout_file.seek(0)
        output_str = stdout_file.read().decode("utf-8", "ignore")
        if output_str:
            log("Output =", output_str)
        else:
            log("No results for the file")
    elif retval == 0:
        log("No issues found")
    else:
        log("Exited with:", retval)
    stdout_file.close()
    return output_str
