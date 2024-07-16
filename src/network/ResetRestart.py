from netsquid import sim_reset
# from src.main import main # cannot be imported here, because it would create a circular dependency
import subprocess


def reset_simulation():
    """Reset the simulation."""
    sim_reset()


def restart_simulation():
    """Restart the simulation."""
    # open the terminal and run the program again
    # cmd = subprocess.run(["pwd"], stdout=subprocess.PIPE, text=True)
    # print(cmd.stdout, "\nExit code: ", cmd.returncode)
    # cmd = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)
    # print(cmd.stdout, "\nExit code: ", cmd.returncode)
    cmd = subprocess.run(["python", "main.py"],
                         # stdout=subprocess.PIPE,
                         # text=True,
                         # check=True
                         )
    # print(cmd.stdout, "\nExit code: ", cmd.returncode)

def reset_and_restart_simulation():
    """Reset and Restart the simulation."""
    reset_simulation()
    restart_simulation()


def check_reset_restart(flag: bool):
    """Check if the reset and restart is required."""
    if flag:
        reset_and_restart_simulation()

    return False
