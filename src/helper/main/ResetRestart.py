from netsquid import sim_reset

from src.helper.terminal.utils import run_command_in_terminal_and_show_output


def reset_simulation() -> None:
    """Reset the simulation."""
    sim_reset()


def restart_simulation(debug: bool = False) -> str:
    """
    Restart the simulation.
    :param debug: The flag to enable the debug mode (default: False)
    :return: The output of the program
    """
    flags = ["text", "stdout"]
    if debug:
        run_command_in_terminal_and_show_output(["pwd"], flags, "Current directory: ")
        run_command_in_terminal_and_show_output(["ls", "-la"], flags, "Files in directory: ")

    program = run_command_in_terminal_and_show_output(["python", "main.py"], flags, "Standard output of the program: ")
    return program


def reset_and_restart_simulation(debug: bool = False) -> str:
    """
    Reset and Restart the simulation.
    :param debug: The flag to enable the debug mode (default: False)
    :return: The output of the program
    """
    reset_simulation()
    out = restart_simulation(debug)
    return out


def check_reset_restart(flag: bool, debug: bool = False) -> bool:
    """
    Check if the reset and restart is required.
    :param flag: The flag to check if the reset and restart is required
    :param debug: The flag to enable the debug mode (default: False)
    :return: The flag, if it is False, the simulation will not be reset and restarted
    """
    if flag:
        reset_and_restart_simulation(debug)
    # return the flag, if it is False, the simulation will not be reset and restarted
    return False
