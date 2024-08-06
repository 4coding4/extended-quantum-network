import unittest

from src.helper.main.ResetRestart import reset_and_restart_simulation, check_reset_restart


class TestHelpersMainResetRestart(unittest.TestCase):
    debug = True

    def test_reset_and_restart_simulation(self):
        out = reset_and_restart_simulation(self.debug)
        self.assertIsNotNone(out)
        # out starts with"Standard output of the program: "
        self.assertTrue(out.startswith("Standard output of the program: "))
        # out contains the followings:
        # ...
        # out ends with "Exit code: "
        # self.assertTrue(out.endswith("Exit code: "))
        print("out:", out)

    def test_check_reset_restart(self):
        new_flag = check_reset_restart(True, self.debug)
        self.assertFalse(new_flag)

        new_flag1 = check_reset_restart(False, self.debug)
        self.assertFalse(new_flag1)
