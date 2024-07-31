import unittest

from netsquid.qubits import create_qubits, ketstates

from src.helper.network.entanglement_swapping_utils.bell_measurement import perform_bell_measurement, \
    print_bell_measurement
from src.helper.network.entanglement_swapping_utils.results import calc_fidelity, get_result
from src.network.StarNetwork import StarNetwork


class TestHelpersNetworkEntanglementSwappingUtilsBellMeasurement(unittest.TestCase):
    qubits = [q0, q1, q2, q3] = create_qubits(num_qubits=4, system_name="Q")  # Create two qubits w default state |0>
    # create a star network
    star_network: StarNetwork = StarNetwork({})
    repeater_memory = star_network.network.subcomponents["Repeater"].qmemory
    # place the qubits in the repeater memory
    repeater_memory.put(qubits)

    m_0_positions = perform_bell_measurement(repeater_memory)
    m_mem_positions = [2, 3]
    m_2_positions = perform_bell_measurement(repeater_memory, m_mem_positions)
    # extract the states in M format
    state_0_positions = m_0_positions[0]["M"][0]
    state_2_positions = m_2_positions[0]["M"][0]

    def test_perform_bell_measurement(self):
        # check that the M values are between 0 and 3
        self.assertTrue(0 <= self.state_0_positions <= 3)
        self.assertTrue(0 <= self.state_2_positions <= 3)
        # extract the key of the M values in the dictionary ('M')
        expected_key = 'M'
        m_0_positions_key = list(self.m_0_positions[0].keys())[0]
        m_2_positions_key = list(self.m_2_positions[0].keys())[0]
        self.assertEqual(expected_key,
                         m_0_positions_key)
        self.assertEqual(expected_key,
                         m_2_positions_key)
        # extract the second position
        expected_second = 0.0
        m_0_positions_second = self.m_0_positions[1]
        m_2_positions_second = self.m_2_positions[1]
        self.assertEqual(expected_second,
                         m_0_positions_second)
        self.assertEqual(expected_second,
                         m_2_positions_second)

    def test_print_bell_measurement(self):
        expected0 = "Bell measurement in repeater:\n" \
                    f"m= {self.m_0_positions}, state:\n" \
                    f"M/Indices format for the states: {self.state_0_positions}\n" \
                    f"B/Bell states/Ket vectors format for the states: {ketstates.BellIndex(self.state_0_positions)}\n"
        self.assertEqual(expected0,
                         print_bell_measurement(self.m_0_positions, self.state_0_positions))

        expected2 = "Bell measurement in repeater:\n" \
                    f"m= {self.m_2_positions}, state:\n" \
                    f"M/Indices format for the states: {self.state_2_positions}\n" \
                    f"B/Bell states/Ket vectors format for the states: {ketstates.BellIndex(self.state_2_positions)}\n"
        self.assertEqual(expected2,
                         print_bell_measurement(self.m_2_positions, self.state_2_positions))


# if __name__ == "__main__":
#     unittest.main()
