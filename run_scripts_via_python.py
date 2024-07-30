# see discussion in
# https://stackoverflow.com/questions/30841383/how-can-i-run-a-shell-script-instead-of-python-in-a-pycharm-run-configuration
# https://youtrack.jetbrains.com/issue/IJPL-531/Command-Line-Run-Configuration
import sys
import subprocess


def show_output_terminal(init_msg: str, cmd: subprocess.CompletedProcess, last_msg: str = "\nExit code: ") -> None:
    """
    Show the output of the command in the terminal;
    it will print the following: the message before, the standard output, the message after, and the exit code.
    :param init_msg: The message to print before the output of the command
    :param cmd: The CompletedProcess of the command that has been run
    :param last_msg: The message before the exit code and after the output of the command
    """
    print(init_msg, cmd.stdout, last_msg, cmd.returncode)


# pass the bash name as an argument to Popen
bash_name = sys.argv[1]

bash = subprocess.run(["./shell_scripts/" + bash_name], stdout=subprocess.PIPE, text=True, shell=True, executable="/bin/bash")
show_output_terminal("bash run: \n", bash)
