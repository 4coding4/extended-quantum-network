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


def run_method_with_nodes(method: callable, nodes: list, debug: bool = False):
    """
    Run the selected method with the provided nodes.
    :param method: callable
    :param nodes: list
    :param debug: bool
    """
    nodes_len = len(nodes)
    # run with the default nodes
    if nodes_len == 0:
        # 1, 2, 4 for protocol_a
        # 1, 4 for entangle_nodes
        fidelity = method(debug=debug)
    # run with the provided nodes
    elif nodes_len == 2:
        # run entangle_nodes
        fidelity = method(nodes[0], nodes[1], debug=debug)
    elif nodes_len == 3:
        # run protocol_a
        fidelity = method(nodes[0], nodes[1], nodes[2], debug=debug)
    else:
        error_exit("Invalid number of nodes, please provide 0 or 2 or 3 nodes")
    print(fidelity)
    return fidelity


def converter_exit(method: callable, input, msg: str):
    """
    Try to convert the input to the desired type, if it fails, exit the program with an error message.
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


def checker(condition: bool, msg: str):
    """
    Check if the condition is True, exit the program with an error message.
    :param condition: bool
    :param msg: str
    """
    if condition:
        error_exit(msg)
