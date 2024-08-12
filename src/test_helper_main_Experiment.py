import os
import unittest

from src.helper.main.Experiment import Experiment
from src.helper.main.main import select_method
from src.network.StarNetwork import StarNetwork


class TestHelpersMainExperiment(unittest.TestCase):
    star_network: StarNetwork = StarNetwork()
    e = Experiment(star_network)

    test_name = "_test"
    out_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../out")

    def test_experiment_setters_getters(self):
        old_num_each_simulation = self.e.num_each_simulation
        self.assertEqual(100, old_num_each_simulation)
        self.e.num_each_simulation = 150
        self.assertEqual(150, self.e.num_each_simulation)

        old_csv_path = self.e.csv_path
        self.assertEqual("../out/data.csv", old_csv_path)
        new_csv = "../out/data" + self.test_name + ".csv"
        self.e.csv_path = new_csv
        self.assertEqual(new_csv, self.e.csv_path)

        old_fig_path = self.e.fig_path
        self.assertEqual("../out/fidelity-over-length.png", old_fig_path)
        new_fig = "../out/fidelity-over-length" + self.test_name + ".png"
        self.e.fig_path = new_fig
        self.assertEqual(new_fig, self.e.fig_path)

    def test_run(self):
        method_name = "protocol_a"
        nodes: list = [1, 2, 4]
        debug: bool = False
        method = select_method(self.star_network, method_name, len(nodes))

        self.e.num_each_simulation = 1
        new_csv = self.out_folder + "/data" + self.test_name + ".csv"
        self.e.csv_path = new_csv
        new_fig = self.out_folder + "/fidelity-over-length" + self.test_name + ".png"
        self.e.fig_path = new_fig

        self.e.run(method, nodes, debug)

        # Check if the CSV file exists and contains the expected data
        csv_file = open(self.e.csv_path)
        lines = csv_file.readlines()
        csv_file.close()

        self.assertEqual(101, len(lines))  # Check if there are 101 lines in the CSV file

        # Check if the png file exists
        fig_file = open(self.e.fig_path, "rb")
        lines = fig_file.readlines()
        fig_file.close()

        self.assertGreater(len(lines), 1)  # Check if there is more than one line in the PNG file

        # delete the csv and png files
        os.remove(self.e.csv_path)
        os.remove(self.e.fig_path)
