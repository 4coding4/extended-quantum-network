from src.helper.error.error import error_exit
from src.models.Combined import Combined
from src.models.Empty import Empty
from src.network.StarNetwork import StarNetwork


def run_method_with_nodes(method: callable, nodes: list, debug: bool = False, test: bool = False):
    """
    Run the selected method with the provided nodes.
    :param method: callable
    :param nodes: list
    :param debug: bool
    :param test: bool (default False)
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
        msg = "Invalid number of nodes, please provide 0 or 2 or 3 nodes"
        return checker(True, msg, test)
    # always print it, since it is the result of the simulation
    print("Results: ", fidelity)
    return fidelity


def checker(condition: bool, msg: str, test: bool = False):
    """
    Check if the condition is True, exit the program with an error message.
    :param condition: bool
    :param msg: str
    :param test: bool (default False)
    """
    if condition:
        if test:
            return msg
        else:
            error_exit(msg)


def show_help() -> str:
    """
    Show the help message with the command line arguments.
    :return: str
    """
    msg = "Command line arguments:"
    msg += "- models_name: str, default='empty', choices=['combined', 'empty']"
    msg += "- method_name: str, default='protocol_a', choices=['protocol_a', 'entangle_nodes']"
    msg += "- nodes: str, default='1,2,4', choices of int=[1, 2, 3, 4], length=[0, 2, 3],"
    msg += "use ',' to separate the nodes (e.g. '1,2,4' or '1,4' or '1,3')"
    msg += "- debug: bool, default=False, if True, print debug information"
    msg += "- experiment_num: int, default=0, if 0, run a single experiment, if >0, run the experiment suite"
    print(msg)
    return msg


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
