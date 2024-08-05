import os
import sys
import unittest

from src.helper.main.main import show_help
from src.main import handle_args, main


class TestMain(unittest.TestCase):
    test_files = ["data[entangle_nodes_empty_[2, 4]_True_1].csv",
                  "fidelity-over-length[entangle_nodes_empty_[2, 4]_True_1].png"]
    out_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../out")

    def test_handle_args(self):
        # inject the command line arguments
        sys.argv = ["main.py", "combined", "protocol_a", "1,2,4", "True", "0"]
        models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main = handle_args()
        self.assertEqual("combined", models_name_main)
        self.assertEqual("protocol_a", method_name_main)
        self.assertEqual([1, 2, 4], nodes_main)
        self.assertTrue(debug_main)
        self.assertEqual(0, experiment_num_main)

        # inject the command line arguments
        sys.argv = ["main.py", "empty", "entangle_nodes", "1,3", "False", "100"]
        models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main = handle_args()
        self.assertEqual("empty", models_name_main)
        self.assertEqual("entangle_nodes", method_name_main)
        self.assertEqual([1, 3], nodes_main)
        self.assertFalse(debug_main)

        # inject the command line arguments
        sys.argv = ["main.py", "empty", "entangle_nodes", "1,3,4", "False", "100"]
        models_name_main, method_name_main, nodes_main, debug_main, experiment_num_main = handle_args()
        self.assertEqual("empty", models_name_main)
        self.assertEqual("entangle_nodes", method_name_main)
        self.assertEqual([1, 3, 4], nodes_main)
        self.assertFalse(debug_main)
        self.assertEqual(100, experiment_num_main)

        # inject the command line arguments
        sys.argv = ["main.py", "help"]
        with self.assertRaises(SystemExit) as cm:
            handle_args()
            self.assertEqual(0, cm.exception.code)
            self.assertEqual(show_help(), cm.exception.args[0].message)
            sys.exit()

    def test_main(self):
        # remove 2 files from the out directory
        for file in self.test_files:
            try:
                os.remove(self.out_folder + f"/{file}")
            except FileNotFoundError:
                pass

        # get list of files in the out directory
        before_files = os.listdir(self.out_folder)
        main(models_name="empty", method_name="entangle_nodes", nodes=[2, 4], debug=True,
             experiment_num=0)
        after_files = os.listdir(self.out_folder)
        self.assertEqual(before_files, after_files)

    def test_main1(self):
        # get list of files in the out directory
        before_files = os.listdir(self.out_folder)
        # before_files not contains the 2 files in test_files
        for file in self.test_files:
            self.assertNotIn(file, before_files)
        main(models_name="empty", method_name="entangle_nodes", nodes=[2, 4], debug=True,
             experiment_num=1)
        after_files = os.listdir(self.out_folder)
        self.assertNotEqual(before_files, after_files)
        # after_files contains the 2 files in test_files
        for file in self.test_files:
            self.assertIn(file, after_files)
