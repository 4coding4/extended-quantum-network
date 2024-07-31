import unittest

from netsquid.qubits import create_qubits

from src.helper.network.entanglement_swapping_utils.results import calc_fidelity, get_result


class TestHelpersNetworkEntanglementSwappingUtilsResults(unittest.TestCase):
    qbits_pair = [q1, q2] = create_qubits(num_qubits=2, system_name="Q")  # Create two qubits w default state |0>

    def test_calc_fidelity(self):
        self.assertEqual(float,
                         type(calc_fidelity(self.qbits_pair)))
        self.assertEqual(0.7071067811865475,
                         calc_fidelity(self.qbits_pair))

    def test_get_results(self):
        self.assertEqual({"qubits": self.qbits_pair, "fidelity": calc_fidelity(self.qbits_pair), "error": False},
                         get_result(self.qbits_pair))


# if __name__ == "__main__":
#     unittest.main()
