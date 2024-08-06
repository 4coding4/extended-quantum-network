# see discussion in
# https://stackoverflow.com/questions/30841383/how-can-i-run-a-shell-script-instead-of-python-in-a-pycharm-run-configuration
# https://youtrack.jetbrains.com/issue/IJPL-531/Command-Line-Run-Configuration
import sys

from src.terminal.terminal_utils import run_command_in_terminal_and_show_output


def run_bash_and_return_outputs(bash_name: str) -> str:
    """
    Run a command in the terminal
    :param bash_name: The name of the bash script to run
    :return: The output of the command
    """
    command = ["./shell_scripts/" + bash_name]
    return run_command_in_terminal_and_show_output(command, ["text", "stdout", "shell", "executable"], "bash run: \n")


if __name__ == "__main__":
    # The first argument is the name of the bash script to run
    run_bash_and_return_outputs(sys.argv[1])
