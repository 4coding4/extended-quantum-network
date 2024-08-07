import os
import unittest

from src.example.entanglement_distribution import network_setup, main


class TestExampleEntanglementDistribution(unittest.TestCase):

    def test_network_setup(self):
        network = network_setup(length=10)
        nodes = [network.get_node(name).name for name in network.nodes]
        self.assertEqual(2, len(network.nodes))
        # nodes contains the following nodes names ['Alice', 'Bob']
        self.assertTrue('Alice' in nodes and 'Bob' in nodes)
        connections = network.connections
        self.assertEqual(1, len(connections))
        connection = network.get_connection(network.get_node('Alice'), network.get_node('Bob'), label="quantum")
        self.assertEqual(connection, connections.get('conn|Alice<->Bob|quantum'))

    def test_main(self):
        verbose = True
        num_each_sim = 1
        csv_file = "test-data.csv"
        plot_file = "test-fidelity-over-length.png"
        # delete the files if they already exist
        files = [csv_file, plot_file]
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

        # run the main function with the provided arguments
        main(verbose=verbose, num_each_sim=num_each_sim, csv_file=csv_file, plot_file=plot_file)

        # check if the files have been created
        self.assertTrue(os.path.isfile(csv_file))
        self.assertTrue(os.path.isfile(plot_file))

        # delete the files after checking
        os.remove(csv_file)
        os.remove(plot_file)
