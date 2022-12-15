from src.models.Combined import Combined
from src.network.StarNetwork import StarNetwork
from src.protocols.Experiment import Experiment


if __name__ == "__main__":
    # Initialize Network and run experiment
    star_network: StarNetwork = StarNetwork(Combined.models)
    Experiment(star_network).run(1, 4)
