import sys

from src.models.Combined import Combined
from src.models.Empty import Empty
from src.network.StarNetwork import StarNetwork


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
        # run entangle_nodes/protocol_a
        fidelity = method(nodes[0], nodes[1], debug=debug)
    elif nodes_len == 3:
        # run protocol_a
        fidelity = method(nodes[0], nodes[1], nodes[2], debug=debug)
    else:
        error_exit("Invalid number of nodes, please provide 0 or 2 or 3 nodes")
    # always print it, since it is the result of the simulation
    print(fidelity)
    return fidelity


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


def checker(condition: bool, msg: str) -> None:
    """
    Check if the condition is True, exit the program with an error message.
    :param condition: bool
    :param msg: str
    """
    if condition:
        error_exit(msg)


def show_help() -> None:
    """
    Show the help message with the command line arguments.
    """
    print("Command line arguments:")
    print("- models_name: str, default='empty', choices=['combined', 'empty']")
    print("- method_name: str, default='protocol_a', choices=['protocol_a', 'entangle_nodes']")
    print("- nodes: str, default='1,2,4', choices of int=[1, 2, 3, 4], length=[0, 2, 3],"
          "use ',' to separate the nodes (e.g. '1,2,4' or '1,4' or '1,3')")
    print("- debug: bool, default=False, if True, print debug information")
    print("- experiment_num: int, default=0, if 0, run a single experiment, if >0, run the experiment suite")


def select_models(models_name_str: str) -> dict:
    """
    Select the models to be used in the network, based on the provided name.
    :param models_name_str: str
    :return: dict of models to be used in the network
    """
    models: dict
    if models_name_str == "combined":
        models = Combined.models
    elif models_name_str == "empty":
        models = Empty.empty_models
    return models


def select_method(star_network: StarNetwork, method_name_str: str, nodes_len) -> callable:
    """
    Select the method to be used in the network, based on the provided name.
    :param star_network: StarNetwork
    :param method_name_str: str
    :param nodes_len: int
    :return: method to be used in the network
    """

    def select_method_uncheck(star_network: StarNetwork, method_name_str: str) -> tuple:
        """
        Select the method to be used in the network, based on the provided name.
        :param star_network: StarNetwork
        :param method_name_str: str
        :return: method to be used in the network and the allowed number of nodes for this method
        """
        method = None
        allowed_nodes_num = [0]
        if method_name_str == "protocol_a":
            method = star_network.protocol_a
            allowed_nodes_num.append(3)
        elif method_name_str == "entangle_nodes":
            method = star_network.entangle_nodes
            allowed_nodes_num.append(2)
        return method, allowed_nodes_num

    method, allowed_nodes_num = select_method_uncheck(star_network, method_name_str)
    # Check if the number of nodes is allowed for the selected method
    checker(nodes_len not in allowed_nodes_num,
            f"Invalid number of nodes, please provide one of the following: {allowed_nodes_num}")
    return method
