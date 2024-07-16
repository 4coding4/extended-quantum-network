from netsquid import sim_reset
# from src.main import main # cannot be imported here, because it would create a circular dependency


def reset_simulation():
    """Reset the simulation."""
    sim_reset()


def restart_simulation():
    """Restart the simulation."""
    # call main in main.py again
    # main()
    # TODO FIND A WAY TO RESTART THE SIMULATION, WITHOUT IMPORTING main() HERE
    # restart the hole program, maybe
    pass


def reset_and_restart_simulation():
    """Reset and Restart the simulation."""
    reset_simulation()
    restart_simulation()


def check_reset_restart(flag: bool):
    """Check if the reset and restart is required."""
    if flag:
        reset_and_restart_simulation()

    return False
