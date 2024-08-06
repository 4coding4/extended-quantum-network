import subprocess


def show_output_terminal(init_msg: str, cmd: subprocess.CompletedProcess, last_msg: str = "\nExit code: ") -> str:
    """
    Show the output of the command in the terminal;
    it will print the following: the message before, the standard output, the message after, and the exit code.
    :param init_msg: The message to print before the output of the command
    :param cmd: The CompletedProcess of the command that has been run
    :param last_msg: The message before the exit code and after the output of the command
    :return: The message that has been printed
    """
    msg = "{}\n{}\n{}{}".format(init_msg, cmd.stdout, last_msg, cmd.returncode)
    print(msg)
    return msg


def run_command_in_terminal(commands: list, flags: list = []) -> subprocess.CompletedProcess:
    """
    Run the command in the terminal
    :param commands: The list of the command to run
    :param flags: The list of the flags to enable (e.g., text, stdout, shell, executable) (default: [])
    :return: The CompletedProcess of the command that has been run
    """

    if (flags.__contains__("text") and flags.__contains__("stdout") and
            flags.__contains__("shell") and flags.__contains__("executable")):
        cmd = subprocess.run(commands, stdout=subprocess.PIPE, text=True, shell=True, executable="/bin/bash")
    elif flags.__contains__("text") and flags.__contains__("stdout"):
        cmd = subprocess.run(commands, stdout=subprocess.PIPE, text=True)
    else:
        cmd = subprocess.run(commands)
    return cmd


def run_command_in_terminal_and_show_output(commands: list, flags: list = [], start_msg: str = "") -> str:
    """
    Run the command in the terminal and show the output in the terminal
    :param commands: The list of the command to run
    :param flags: The list of the flags to enable (e.g., text, stdout, shell, executable) (default: [])
    :param start_msg: The message to print before the output of the command
    :return: The message that has been printed
    """
    cmd = run_command_in_terminal(commands, flags)
    return show_output_terminal(start_msg, cmd)
