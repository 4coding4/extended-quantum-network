import sys

from src.models.Combined import Combined
from src.models.Empty import Empty
from src.network.ResetRestart import check_reset_restart
from src.network.StarNetwork import StarNetwork
from src.protocols.Experiment import Experiment


def select_models(models_name: str) -> dict:
    """
    Select the models to be used in the network, based on the provided name.
    :param models_name: str
    :return: dict of models to be used in the network
    """
    models: dict
    if models_name == "combined":
        models = Combined.models
    elif models_name == "empty":
        models = Empty.empty_models
    return models


def select_method(star_network: StarNetwork, method_name: str) -> callable:
    """
    Select the method to be used in the network, based on the provided name.
    :param star_network: StarNetwork
    :param method_name: str
    :return: method to be used in the network and the allowed number of nodes for this method
    """
    method = None
    allowed_nodes_num = [0]
    if method_name == "protocol_a":
        method = star_network.protocol_a
        allowed_nodes_num.append(3)
    elif method_name == "entangle_nodes":
        method = star_network.entangle_nodes
        allowed_nodes_num.append(2)
    return method, allowed_nodes_num


def main(models_name, method_name, nodes=[], debug=False, experiment_num=0):
    """
    Main function to run the simulation.
    """
    global reset_restart
    reset_restart = False

    nodes_len = len(nodes)
    # Initialize Network and run experiment
    models: dict = select_models(models_name)
    star_network: StarNetwork = StarNetwork(models)
    # Select the method to be used in the network
    method, allowed_nodes_num = select_method(star_network, method_name)
    # Check if the number of nodes is allowed for the selected method
    if nodes_len not in allowed_nodes_num:
        print(f"Invalid number of nodes, please provide one of the following: {allowed_nodes_num}")
        return
    # Run single experiment
    # ---------------------
    if experiment_num == 0:
        # run with the default nodes
        if nodes_len == 0:
            # 1, 2, 4 for protocol_a
            # 1, 4 for entangle_nodes
            fidelity = method(debug=debug)
            print(fidelity)
        # run with the provided nodes
        elif nodes_len == 2:
            # run entangle_nodes
            fidelity = method(nodes[0], nodes[1], debug=debug)
            print(fidelity)
        elif nodes_len == 3:
            # run protocol_a
            fidelity = method(nodes[0], nodes[1], nodes[2], debug=debug)
            print(fidelity)

        # reset restart simulation
        reset_restart = False  # True
        reset_restart = check_reset_restart(reset_restart)
    else:
        # TODO idk if this is needed/required, if required pass to experiment the method and the nodes (partial rewrite needed)
        pass
        # Run experiment suite (Node1 *-* Node2)
        # --------------------------------------
        # experiment: Experiment = Experiment(star_network, verbose=False)
        # experiment.csv_path = "../out/data[node-node].csv"
        # experiment.fig_path = "../out/fidelity-over-length[node-node].png"
        # experiment.run(1, 3)

        # Run experiment suite (Node1 *-* RemoteNode)
        # -------------------------------------------
        # experiment: Experiment = Experiment(star_network, verbose=False)
        # experiment.csv_path = f"../out/data[node-remote].csv"
        # experiment.fig_path = f"../out/fidelity-over-length[node-remote].png"
        # experiment.run(1, 4)


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


def handle_args() -> tuple[str, str, list[int], bool, int]:
    """
    Handle the command line arguments.
    """
    if sys.argv[1] == "help":
        show_help()
        sys.exit()
    # make the following variables the default values
    global models_name, method_name, nodes, debug, experiment_num
    models_name: str = "empty"
    method_name: str = "protocol_a"
    nodes: list[int] = [1, 2, 4]
    debug: bool = False
    experiment_num: int = 0
    for i in range(1, len(sys.argv)):
        if i == 1:
            models_name = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            if models_name not in ["combined", "empty"]:
                print("Invalid models_name, please provide 'combined' or 'empty'")
                sys.exit()
        elif i == 2:
            method_name = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            if method_name not in ["protocol_a", "entangle_nodes"]:
                print("Invalid method_name, please provide 'protocol_a' or 'entangle_nodes'")
                sys.exit()
        elif i == 3:
            try:
                nodes_str: list[str] = sys.argv[i].split(",")
                # convert the strings to integers
                nodes = [int(node) for node in nodes_str]
            except ValueError:
                print("Invalid nodes, please provide a list of integers separated by ','")
                sys.exit()

            # check that nodes is a list of non-duplicate integers (between 1 and 4) and the length is either 0, 2 or 3
            if len(nodes) not in [0, 2, 3]:
                print("Invalid number of nodes, please provide a list of length 0, 2 or 3")
                sys.exit()
            if len(nodes) != len(set(nodes)):
                print("Invalid nodes, please provide a list of unique integers")
                sys.exit()
            if any(node < 1 or node > 4 for node in nodes):
                print("Invalid nodes, please provide a list of integers between 1 and 4")
                sys.exit()
        elif i == 4:
            debug_str = sys.argv[i]
            # convert the string to a boolean
            if debug_str == "True":
                debug = True
            elif debug_str == "False":
                debug = False
            else:
                print("Invalid debug, please provide 'True' or 'False'")
                sys.exit()
        elif i == 5:
            try:
                experiment_num = int(sys.argv[i])
            except ValueError:
                print("Invalid experiment_num, please provide an integer")
                sys.exit()

    return models_name, method_name, nodes, debug, experiment_num


if __name__ == "__main__":
    # handle the command line arguments
    models_name, method_name, nodes, debug, experiment_num = handle_args()

    # print all the parsed arguments
    print("Parsed arguments:")
    print(f"models_name: {models_name}")
    print(f"method_name: {method_name}")
    print(f"nodes: {nodes}")
    print(f"debug: {debug}")
    print(f"experiment_num: {experiment_num}")

    # run the main function
    main(models_name, method_name, nodes, debug, experiment_num)

    # test entangle_nodes
    # main(models_name="empty", method_name="entangle_nodes", nodes=[1, 3])
    # default nodes 1, 4
    # main(models_name="empty", method_name="entangle_nodes")
    # test protocol_a
    # default nodes 1, 2, 4
    # main(models_name="empty", method_name="protocol_a", debug=True)
    # main(models_name="combined", method_name="protocol_a", debug=True) # use this at the end to run w noises/errors
