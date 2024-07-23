from src.helper.main_helper import error_exit


def converter_exit(method: callable, input: any, msg: str) -> any:
    """
    Try to convert the input to the desired type, if it fails, exit the program with an error message.
    :param method: callable
    :param input: any
    :param msg: str
    :return: any
    """
    output, error = method(input)
    if error:
        error_exit(msg)
    else:
        return output


def converter_string_boolean(input: str) -> tuple:
    """
    Convert the input string to a boolean.
    :param input: str
    :return: tuple of boolean and error
    """
    if input == "True":
        return True, False
    elif input == "False":
        return False, False
    else:
        return None, True


def converter_string_int(input: str) -> tuple:
    """
    Convert the input string to an integer.
    :param input: str
    :return: tuple of integer and error
    """
    try:
        return int(input), False
    except ValueError:
        return None, True


def converter_string_list_int(input: str) -> tuple:
    """
    Convert the input string to a list of integers.
    :param input: str
    :return: tuple of list of integers and error
    """
    try:
        return [int(node) for node in input.split(",")], False
    except ValueError:
        return None, True
    