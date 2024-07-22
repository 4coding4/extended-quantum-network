import sys

from src.helper.main_helper import error_exit, run_method_with_nodes
from src.models.Combined import Combined
from src.models.Empty import Empty
from src.network.ResetRestart import check_reset_restart
from src.network.StarNetwork import StarNetwork
from src.protocols.Experiment import Experiment


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


def select_method(star_network: StarNetwork, method_name_str: str) -> callable:
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


def main(models_name: str, method_name: str, nodes: list = [], debug: bool = False, experiment_num: int = 0):
    """
    Main function to run the simulation.
    """
    nodes_len = len(nodes)
    # Initialize Network and run experiment
    models: dict = select_models(models_name)
    star_network: StarNetwork = StarNetwork(models)
    # Select the method to be used in the network
    method, allowed_nodes_num = select_method(star_network, method_name)
    # Check if the number of nodes is allowed for the selected method
    if nodes_len not in allowed_nodes_num:
        error_exit(f"Invalid number of nodes, please provide one of the following: {allowed_nodes_num}")
    if experiment_num < 0:
        error_exit("Invalid experiment_num, please provide a non-negative integer")
    # Run single experiment
    # ---------------------
    if experiment_num == 0:
        _ = run_method_with_nodes(method, nodes, debug)
    else:
        # TODO idk if this is needed/required, if required pass to experiment the method and the nodes (partial rewrite needed)
        underscore = "_"
        run_name = (method_name + underscore + models_name + underscore + str(nodes)
                    + underscore + str(debug) + underscore + str(experiment_num))
        experiment: Experiment = Experiment(star_network, verbose=debug)
        experiment.csv_path = f"../out/data[{run_name}].csv"
        experiment.fig_path = f"../out/fidelity-over-length[{run_name}].png"
        experiment.num_each_simulation = experiment_num  # set the number of measurements for each run of the simulation
        experiment.run(method, nodes, debug)
    # reset restart simulation
    reset_restart = False  # True
    reset_restart = check_reset_restart(reset_restart)


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


def handle_args() -> tuple:
    """
    Handle the command line arguments.
    """
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        show_help()
        sys.exit()
    # make the following variables the default values
    # global models_name, method_name, nodes, debug, experiment_num
    models_name_input: str = "empty"  # "combined"
    method_name_input: str = "protocol_a"  # "entangle_nodes"
    nodes_input: list[int] = [1, 2, 4]  # [1,4]
    debug_input: bool = True
    experiment_num_input: int = 100
    for i in range(1, len(sys.argv)):
        if i == 1:
            models_name_input = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            if models_name_input not in ["combined", "empty"]:
                error_exit("Invalid models_name, please provide 'combined' or 'empty'")
        elif i == 2:
            method_name_input = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            if method_name_input not in ["protocol_a", "entangle_nodes"]:
                error_exit("Invalid method_name, please provide 'protocol_a' or 'entangle_nodes'")
        elif i == 3:
            try:
                nodes_str: list[str] = sys.argv[i].split(",")
                # convert the strings to integers
                nodes_input = [int(node) for node in nodes_str]
            except ValueError:
                error_exit("Invalid nodes, please provide a list of integers separated by ','")

            # check that nodes is a list of non-duplicate integers (between 1 and 4) and the length is either 0, 2 or 3
            if len(nodes_input) not in [0, 2, 3]:
                error_exit("Invalid number of nodes, please provide a list of length 0, 2 or 3")
            if len(nodes_input) != len(set(nodes_input)):
                error_exit("Invalid nodes, please provide a list of unique integers")
            if any(node < 1 or node > 4 for node in nodes_input):
                error_exit("Invalid nodes, please provide a list of integers between 1 and 4")
        elif i == 4:
            debug_str = sys.argv[i]
            # convert the string to a boolean
            if debug_str == "True":
                debug_input = True
            elif debug_str == "False":
                debug_input = False
            else:
                error_exit("Invalid debug, please provide 'True' or 'False'")
        elif i == 5:
            try:
                experiment_num_input = int(sys.argv[i])
            except ValueError:
                error_exit("Invalid experiment_num, please provide an integer")

    return models_name_input, method_name_input, nodes_input, debug_input, experiment_num_input


if __name__ == "__main__":
    # handle the command line arguments
    models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main = handle_args()

    # print all the parsed arguments
    print("Parsed arguments:")
    print(f"models_name: {models_name_main}")
    print(f"method_name: {method_name_main}")
    print(f"nodes: {nodes_main}")
    print(f"debug: {debug_main}")
    print(f"experiment_num: {experiment_num_main}")

    # run the main function
    main(models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main)

    # test entangle_nodes
    # main(models_name="empty", method_name="entangle_nodes", nodes=[1, 3]) # crash ?
    # default nodes 1, 4
    # main(models_name="empty", method_name="entangle_nodes")
    # test protocol_a
    # default nodes 1, 2, 4
    # main(models_name="empty", method_name="protocol_a", debug=True)
    # main(models_name="combined", method_name="protocol_a", debug=True) # use this at the end to run w noises/errors
