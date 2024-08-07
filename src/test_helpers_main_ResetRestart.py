import unittest

from src.helper.main.ResetRestart import reset_and_restart_simulation, check_reset_restart


class TestHelpersMainResetRestart(unittest.TestCase):
    # Needed to fix the path of the main.py in restart_simulation function, when run all the tests
    # (but not the single test/class)
    debug = True

    def test_reset_and_restart_simulation(self):
        out = reset_and_restart_simulation(self.debug)
        self.assertIsNotNone(out)
        # out starts with"Standard output of the program: "
        self.assertTrue(out.startswith("Standard output of the program: "))
        # out contains the followings:
        self.assertIn("Parsed arguments:", out)
        self.assertIn("If it is working correctly, the output should have 4 Qubits and 4 None", out)
        self.assertIn("If it is working correctly, the output should have all Qubits and 0 None", out)
        self.assertIn("Bell measurement in repeater:", out)
        self.assertIn("After entanglement swapping:", out)
        self.assertIn("If it is working correctly, the output should have all None", out)
        # out ends with "Exit code: "
        self.assertTrue(out.endswith("Exit code: 0"))

    def test_check_reset_restart(self):
        new_flag = check_reset_restart(True, self.debug)
        self.assertFalse(new_flag)

        new_flag1 = check_reset_restart(False, self.debug)
        self.assertFalse(new_flag1)
