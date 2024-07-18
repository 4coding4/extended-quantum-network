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
    models = select_models(models_name)
    star_network: StarNetwork = StarNetwork(models)

    method, allowed_nodes_num = select_method(star_network, method_name)

    # Check if the number of nodes is allowed
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


if __name__ == "__main__":
    # TODO accept command line arguments to choose between (combined and empty) models and the number to run the experiment on (optional)

    # TODO add checks to the cmd arguments:
    # check that models_name is either "combined" or "empty"
    # check that method_name is either "protocol_a" or "entangle_nodes"
    # check that nodes is a list of non duplicate integers (between 1 and 4) and the length is either 0, 2 or 3

    # test entangle_nodes
    # main(models_name="empty", method_name="entangle_nodes", nodes=[1, 3])
    # default nodes 1, 4
    # main(models_name="empty", method_name="entangle_nodes")
    # test protocol_a
    # default nodes 1, 2, 4
    main(models_name="empty", method_name="protocol_a", debug=True)
    # main(models_name="combined", method_name="protocol_a", debug=True) # TODO reactivate this at the end to enable noises/errors
