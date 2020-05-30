from contextlib import contextmanager
from io import StringIO

class CapturedText(object):
    pass

@contextmanager
def captured(disallow_stderr=True):
    """
    Context manager to capture the printed output of the code in the with block

    Bind the context manager to a variable using `as` and the result will be
    in the stdout property.

    >>> from tests.helpers import capture
    >>> with captured() as c:
    ...     print('hello world!')
    ...
    >>> c.stdout
    'hello world!\n'
    """
    import sys

    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = outfile = StringIO()
    sys.stderr = errfile = StringIO()
    c = CapturedText()
    yield c
    c.stdout = outfile.getvalue()
    c.stderr = errfile.getvalue()
    sys.stdout = stdout
    sys.stderr = stderr
    if disallow_stderr and c.stderr:
        raise Exception("Got stderr output: %s" % c.stderr)