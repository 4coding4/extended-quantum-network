from netsquid import b00, qubits
from netsquid.components import INSTR_X, INSTR_Z
from netsquid.components.qmemory import Qubit
from netsquid.qubits import ketstates, QRepr
from typing import List, Dict, Union


def apply_gates(curr_state: int, remote_node_memory, position: int = -1, debug: bool=False) -> None:
    """
    Apply the necessary gates to the qubit in the memory position (in the RemoteNode),
    based on the state (in the repeater).
    :param curr_state: The state of the qubit in the Repeater memory position, w M format(0, 1, 2, or 3)
    :param position: The memory position in the RemoteNode (0 or 1)
    :param remote_node_memory: The memory of the RemoteNode
    :param debug: A flag to print the steps of the function
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
    for instr in get_instructions:
        if position == -1:
            remote_node_memory.execute_instruction(instr)
        else:
            remote_node_memory.execute_instruction(instr, [position])
            # , output_key="M" , inplace=True, repetitions=1, position=position)  # position=position
        if debug:
            msg = f"Applying instruction {instr} to the qubit "
            if position != -1:
                msg += f"in memory position {position} in the RemoteNode"
            print(msg)


def print_bell_measurement(m, state) :
    """
    Print the measurement of the Bell state and the state of the qubit in the Repeater
    :param m: The measurement of the Bell state
    :param state: The state of the qubit in the Repeater
    """
    print('Bell measurement in repeater:')
    print('m= ', m, ', state:')
    print('M/Indices format for the states: ', state)
    print('B/Bell states/Ket vectors format for the states: ', ketstates.BellIndex(state))


def calc_fidelity(pair1: List[Qubit], reference_state: QRepr = b00) \
        -> float:
    """
    Calculate the fidelity between the pairs of qubits.

    :param pair1: The first pair of qubits
    :param reference_state: The reference state to compare the fidelity to
    :return: The fidelity of the pair of qubits
    """
    return qubits.fidelity(pair1, reference_state)


def get_result(pair: List[Qubit]) -> Dict[str, Union[List[Qubit], float, bool]]:
    """
    Get the result of the entanglement swapping protocol.

    :param pair: The pair of qubits
    :return: A dictionary with the results of the entanglement swapping protocol
    """
    fidelity = calc_fidelity(pair)
    result = {"qubits": pair, "fidelity": fidelity, "error": False}
    return result


def get_results(pair1: List[Qubit], pair2: List[Qubit]) -> List[Dict[str, Union[List[Qubit], float, bool]]]:
    """
    Get the results of the entanglement swapping protocol.

    :param pair1: The first pair of qubits
    :param pair2: The second pair of qubits
    :return: A list with the results of the entanglement swapping protocol
    """
    result1 = get_result(pair1)
    result2 = get_result(pair2)
    return [result1, result2]
