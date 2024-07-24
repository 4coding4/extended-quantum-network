import sys


def error_exit(msg: str) -> None:
    """
    Exit the program with an error message and exit code 1.
    :param msg: str
    """
    # Quote from the documentation
    # sys.exit("some error message") is a quick way to exit a program when an error occurs.
    # https://docs.python.org/3.11/library/sys.html#sys.exit
    sys.exit(msg)
