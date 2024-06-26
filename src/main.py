from src.models.Combined import Combined
from src.network.StarNetwork import StarNetwork
from src.protocols.Experiment import Experiment


if __name__ == "__main__":
    # Initialize Network and run experiment
    star_network: StarNetwork = StarNetwork(Combined.models)


    # Run single experiment
    # ---------------------
    # fidelity = star_network.entangle_nodes(1, 3)
    # print(fidelity)
    fidelity = star_network.entangle_nodes(1, 4)
    print(fidelity)

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
