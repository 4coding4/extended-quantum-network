from netsquid.components import INSTR_X, INSTR_Z
from netsquid.components.qmemory import Qubit
from typing import List, Dict, Union

from src.helper.error.error import error_exit
from src.helper.network.entanglement_swapping_utils.bell_measurement import perform_bell_measurement, \
    print_bell_measurement
from src.helper.network.entanglement_swapping_utils.results import get_result


def apply_gates(curr_state: int, remote_node_memory, position: int = -1, debug: bool = False) -> str:
    """
    Apply the necessary gates to the qubit in the memory position (in the RemoteNode),
    based on the state (in the repeater).
    :param curr_state: The state of the qubit in the Repeater memory position, w M format(0, 1, 2, or 3)
    :param remote_node_memory: The memory of the RemoteNode
    :param position: The memory position in the RemoteNode (0 or 1) where the qubit is stored,
    -1 if not specified (default)
    :param debug: A flag to print the steps of the function
    :return: The message with the steps of the function
    """
    # dictionary with the instructions to apply based on the state of the qubit
    # (represented w numbers, input of the function curr_state or as bell states in the comments)
    instructions = {
        0: [],  # |00> (no gates to apply)
        1: [INSTR_X],  # |01>
        2: [INSTR_Z, INSTR_X],  # |11>
        3: [INSTR_Z]  # |10>
    }
    # get the instructions based on the state of the qubit in the memory position
    get_instructions = instructions[curr_state]
    # apply the instructions to the qubit in the memory position (in the RemoteNode)
    msg = ''
    for instr in get_instructions:
        if position == -1:
            remote_node_memory.execute_instruction(instr)
        else:
            remote_node_memory.execute_instruction(instr, [position])
            # , output_key="M" , inplace=True, repetitions=1, position=position)  # position=position
        if debug:
            msg += f"Applying instruction {instr} to the qubit "
            if position != -1:
                msg += f"in memory position {position} in the RemoteNode, "
    if debug:
        print(msg)
    return msg


def perform_and_get_bell_measurement_w_state(remote_node_memory, positions: list = [],
                                             debug: bool = False):
    """
    Perform the Bell measurement in the Repeater.
    :param remote_node_memory: The memory of the RemoteNode
    :param positions: The memory positions in the RemoteNode where the qubits are stored
    :param debug: A flag to print the results of the function
    :return: The measurement of the Bell state and the state of the qubit in the Repeater
    """
    m = perform_bell_measurement(remote_node_memory, positions)
    # Get the state of the qubit in the Repeater
    state = m[0]["M"][0]
    if debug:
        print_bell_measurement(m, state)
    return m, state


def get_results(pairs: List[List[Qubit]]) -> List[Dict[str, Union[List[Qubit], float, bool]]]:
    """
    Get the results of the entanglement swapping protocol.

    :param pairs: The pairs of qubits
    :return: A list with the results of the entanglement swapping protocol
    """
    results = []
    for pair in pairs:
        results.append(get_result(pair))
    return results


def get_results_qubits(qubits: List[Qubit]) -> List[Dict[str, Union[List[Qubit], float, bool]]]:
    """
    Get the results of the entanglement swapping protocol.

    :param qubits: qubits
    :return: A list with the results of the entanglement swapping protocol
    """
    length = len(qubits)
    pairs = []
    if length == 2:
        # pair = [qubit_node1, qubit_node2]
        pair = [qubits[0], qubits[1]]
        pairs.append(pair)
    elif length == 4:
        # channel_1_pair = [qubit_node1, qubit_node3_1]
        # channel_0_pair = [qubit_node2, qubit_node3]
        # results = get_results([channel_1_pair, channel_0_pair])
        pair1 = [qubits[0], qubits[3]]
        pair2 = [qubits[1], qubits[2]]
        pairs.append(pair1)
        pairs.append(pair2)
    else:
        error_exit("Invalid number of qubits in get_results_qubits")

    return get_results(pairs)
