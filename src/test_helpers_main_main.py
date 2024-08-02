import unittest

from src.helper.main.main import run_method_with_nodes, show_help, select_models
from src.models.Combined import Combined
from src.models.Empty import Empty


class TestHelpersMainMain(unittest.TestCase):

    def test_run_method_with_nodes(self):
        # create callable functions for testing
        def method(node1: int = 0, node2: int = 0, node3: int = 0, debug: bool = False) -> float:
            return node1 + node2 + node3

        self.assertEqual(0,
                         run_method_with_nodes(method, []))
        self.assertEqual(2,
                         run_method_with_nodes(method, [1, 1]))
        self.assertEqual(3,
                         run_method_with_nodes(method, [1, 1, 1]))
        self.assertEqual("Invalid number of nodes, please provide 0 or 2 or 3 nodes",
                         run_method_with_nodes(method, [1, 1, 1, 1], True, True))

    # skipped since previous tests are sufficient
    # def test_checker(self):

    def test_show_help(self):
        self.assertEqual("Command line arguments:- models_name: str, default='empty', choices=['combined', 'empty']- "
                         "method_name: str, default='protocol_a', choices=['protocol_a', 'entangle_nodes']- nodes: "
                         "str, default='1,2,4', choices of int=[1, 2, 3, 4], length=[0, 2, 3],use ',' to separate the "
                         "nodes (e.g. '1,2,4' or '1,4' or '1,3')- debug: bool, default=False, if True, print debug "
                         "information- experiment_num: int, default=0, if 0, run a single experiment, if >0, "
                         "run the experiment suite",
                         show_help())

    def test_select_models(self):
        self.assertEqual("Invalid models name, please provide one of the following: ['combined', 'empty']",
                         select_models("invalid", True))
        self.assertEqual(Combined.models,
                         select_models("combined"))
        self.assertEqual(Empty.empty_models,
                         select_models("empty"))


if __name__ == "__main__":
    unittest.main()
