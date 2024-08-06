from netsquid import sim_reset
import subprocess

from src.terminal.terminal_utils import show_output_terminal, run_command_in_terminal_and_show_output


def reset_simulation() -> None:
    """Reset the simulation."""
    sim_reset()


def restart_simulation(show_output: bool = False, debug: bool = False) -> None:
    """Restart the simulation."""
    # open the terminal and show the current directory and the files in it
    if debug:
        flags = ["text", "stdout"]
        pwd = run_command_in_terminal_and_show_output(["pwd"], flags, "Current directory: ")
        # current_directory = subprocess.run(["pwd"], stdout=subprocess.PIPE, text=True)
        # show_output_terminal("Current directory: ", current_directory)
        # files = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)
        # show_output_terminal("Files in directory: ", files)
        files = run_command_in_terminal_and_show_output(["ls", "-la"], flags, "Files in directory: ")
    # open the terminal and run the program again
    # program = subprocess.run(["python", "main.py"])
    # if show_output:
    #     show_output_terminal("Standard output of the program: ", program)
    program = run_command_in_terminal_and_show_output(["python", "main.py"], [], "Standard output of the program: ")
    return program


def reset_and_restart_simulation(debug: bool = False) -> None:
    """Reset and Restart the simulation."""
    reset_simulation()
    restart_simulation()


def check_reset_restart(flag: bool) -> bool:
    """Check if the reset and restart is required."""
    if flag:
        reset_and_restart_simulation()
    # return the flag, if it is False, the simulation will not be reset and restarted
    return False
