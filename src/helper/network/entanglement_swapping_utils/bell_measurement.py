from netsquid.components import INSTR_MEASURE_BELL
from netsquid.qubits import ketstates


def perform_bell_measurement(remote_node_memory, positions: list = []):
    """
    Perform the Bell measurement in the Repeater.
    :param remote_node_memory: The memory of the RemoteNode
    :param positions: The memory positions in the RemoteNode where the qubits are stored
    :return: The measurement of the Bell state
    """
    # Perform the Bell measurement in the Repeater
    if len(positions) == 0:
        m = remote_node_memory.execute_instruction(INSTR_MEASURE_BELL, output_key="M")
    else:
        m = remote_node_memory.execute_instruction(INSTR_MEASURE_BELL, positions, output_key="M")
    return m


def print_bell_measurement(m, state) -> str:
    """
    Print the measurement of the Bell state and the state of the qubit in the Repeater
    :param m: The measurement of the Bell state
    :param state: The state of the qubit in the Repeater
    :return: The message with the measurement of the Bell state and the state of the qubit in the Repeater
    """
    msg = 'Bell measurement in repeater:\n'
    msg += f'm= {m}, state:\n'
    msg += f'M/Indices format for the states: {state}\n'
    msg += f'B/Bell states/Ket vectors format for the states: {ketstates.BellIndex(state)}\n'
    print(msg)
    return msg
