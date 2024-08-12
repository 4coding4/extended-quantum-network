import unittest

from run_scripts_via_python import run_bash_and_return_outputs


class TestRunScriptsViaPython(unittest.TestCase):
    def test_run_code_lint(self):
        bash_name = "code_lint.sh"
        out = run_bash_and_return_outputs(bash_name)
        self.assertIn("bash run:", out)
        self.assertIn("Exit code: ", out)

    def test_run_generate_req(self):
        bash_name = "generate_req.sh"
        out = run_bash_and_return_outputs(bash_name, [])  # no flags needed
        self.assertEqual('bash run: \n\nNone\n\nExit code: 0', out)

# via this, the function above cannot file the bash script, but by running coverage.sh it works as expected
