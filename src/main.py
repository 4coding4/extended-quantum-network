import sys

from src.helper.main.converter.converter import converter_exit, converter_string_list_int, converter_string_boolean, \
    converter_string_int
from src.helper.main.main import run_method_with_nodes, checker, show_help, select_models, select_method
from src.helper.main.ResetRestart import check_reset_restart
from src.network.StarNetwork import StarNetwork
from src.helper.main.Experiment import Experiment


def main(models_name: str, method_name: str, nodes: list = [], debug: bool = False, experiment_num: int = 0):
    """
    Main function to run the simulation.
    """
    # Initialize Network and run experiment
    models: dict = select_models(models_name)
    star_network: StarNetwork = StarNetwork(models)
    # Select the method to be used in the network
    method = select_method(star_network, method_name, len(nodes))
    # Run single experiment
    # ---------------------
    if experiment_num == 0:
        _ = run_method_with_nodes(method, nodes, debug)
    else:
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
    debug_input: bool = True  # False
    experiment_num_input: int = 0  # 100
    for i in range(1, len(sys.argv)):
        if i == 1:
            models_name_input = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            checker(models_name_input not in ["combined", "empty"],
                    "Invalid models_name, please provide 'combined' or 'empty'")
        elif i == 2:
            method_name_input = sys.argv[i]
            # check that models_name is either "combined" or "empty"
            checker(method_name_input not in ["protocol_a", "entangle_nodes"],
                    "Invalid method_name, please provide 'protocol_a' or 'entangle_nodes'")
        elif i == 3:
            nodes_input = converter_exit(converter_string_list_int, sys.argv[i],
                                         "Invalid nodes, please provide a list of integers separated by ','")

            # check that nodes is a list of non-duplicate integers (between 1 and 4) and the length is either 0, 2 or 3
            checker(len(nodes_input) not in [0, 2, 3],
                    "Invalid number of nodes, please provide a list of length 0, 2 or 3")
            checker(len(nodes_input) != len(set(nodes_input)),
                    "Invalid nodes, please provide a list of unique integers")
            checker(any(node < 1 or node > 4 for node in nodes_input),
                    "Invalid nodes, please provide a list of integers between 1 and 4")
        elif i == 4:
            debug_input = converter_exit(converter_string_boolean, sys.argv[i],
                                         "Invalid debug, please provide 'True' or 'False")
        elif i == 5:
            experiment_num_input = converter_exit(converter_string_int, sys.argv[i],
                                                  "Invalid experiment_num, please provide an integer")
            checker(experiment_num_input < 0,
                    "Invalid experiment_num, please provide a non-negative integer")

    return models_name_input, method_name_input, nodes_input, debug_input, experiment_num_input


if __name__ == "__main__":
    # handle the command line arguments
    models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main = handle_args()

    # print all the parsed arguments
    if debug_main:
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
