from netsquid import b00, qubits
from netsquid.components.qmemory import Qubit
from netsquid.qubits import QRepr
from typing import List, Dict, Union


def calc_fidelity(pair1: List[Qubit], reference_state: QRepr = b00) -> float:
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
