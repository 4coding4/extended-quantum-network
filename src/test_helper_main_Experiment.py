import unittest

from src.helper.main.Experiment import Experiment
from src.network.StarNetwork import StarNetwork


class TestHelpersMainExperiment(unittest.TestCase):
    e = Experiment(StarNetwork())

    def test_experiment_setters_getters(self):
        old_num_each_simulation = self.e.num_each_simulation
        self.assertEqual(100, old_num_each_simulation)
        self.e.num_each_simulation = 150
        self.assertEqual(150, self.e.num_each_simulation)

        old_csv_path = self.e.csv_path
        self.assertEqual("../out/data.csv", old_csv_path)
        self.e.csv_path = "../out/data_df.csv"
        self.assertEqual("../out/data_df.csv", self.e.csv_path)

        old_fig_path = self.e.fig_path
        self.assertEqual("../out/fidelity-over-length.png", old_fig_path)
        self.e.fig_path = "../out/fidelity-over-length_img.png"
        self.assertEqual("../out/fidelity-over-length_img.png", self.e.fig_path)
