from src.models.Combined import Combined
from src.models.Empty import Empty
from src.network.ResetRestart import check_reset_restart
from src.network.StarNetwork import StarNetwork
from src.protocols.Experiment import Experiment


def main():
    """
    Main function to run the simulation.
    """
    global reset
    reset = False
    # Initialize Network and run experiment
    # star_network: StarNetwork = StarNetwork(Combined.models)  # TODO reactivate this at the end to enable noises/errors
    star_network: StarNetwork = StarNetwork(Empty.empty_models)

    # Run single experiment
    # ---------------------
    # fidelity = star_network.entangle_nodes(1, 3)
    # print(fidelity)
    # fidelity = star_network.entangle_nodes(1, 4)
    # print(fidelity)
    fidelity = star_network.protocol_a()  # 1, 2, 4
    print(fidelity)
    reset = True
    reset = check_reset_restart(reset)
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
    main()
