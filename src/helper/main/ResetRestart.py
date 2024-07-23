from netsquid import sim_reset
import subprocess


def reset_simulation() -> None:
    """Reset the simulation."""
    sim_reset()


def restart_simulation(show_output: bool = False, debug: bool = False) -> None:
    """Restart the simulation."""

    def show_output_terminal(init_msg: str, cmd: subprocess.CompletedProcess, last_msg: str = "\nExit code: ") -> None:
        """
        Show the output of the command in the terminal;
        it will print the following: the message before, the standard output, the message after, and the exit code.
        :param init_msg: The message to print before the output of the command
        :param cmd: The CompletedProcess of the command that has been run
        :param last_msg: The message before the exit code and after the output of the command
        """
        print(init_msg, cmd.stdout, last_msg, cmd.returncode)

    # open the terminal and show the current directory and the files in it
    if debug:
        current_directory = subprocess.run(["pwd"], stdout=subprocess.PIPE, text=True)
        show_output_terminal("Current directory: ", current_directory)
        files = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)
        show_output_terminal("Files in directory: ", files)
    # open the terminal and run the program again
    program = subprocess.run(["python", "main.py"])
    if show_output:
        show_output_terminal("Standard output of the program: ", program)


def reset_and_restart_simulation() -> None:
    """Reset and Restart the simulation."""
    reset_simulation()
    restart_simulation()


def check_reset_restart(flag: bool) -> bool:
    """Check if the reset and restart is required."""
    if flag:
        reset_and_restart_simulation()
    # return the flag, if it is False, the simulation will not be reset and restarted
    return False
